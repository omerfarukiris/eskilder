"""Görsel küçültme ve paylaşım (Open Graph) görseli üretimi."""
import io
import os

from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from PIL import Image, ImageOps, UnidentifiedImageError

HATA_MESAJI = "Bu görsel biçimi desteklenmiyor. Lütfen JPG veya PNG yükleyin."
PAYLASIM_BOYUT = (1200, 630)
PAYLASIM_UST_SINIR = 300 * 1024


class GorselHatasi(ValidationError):
    def __init__(self, mesaj=HATA_MESAJI):
        super().__init__(mesaj)


def _ac(dosya) -> Image.Image:
    try:
        dosya.seek(0)
        resim = Image.open(dosya)
        resim.load()
    except (UnidentifiedImageError, OSError, ValueError, Image.DecompressionBombError) as hata:
        raise GorselHatasi() from hata
    return ImageOps.exif_transpose(resim)


def _seffaf_mi(resim: Image.Image) -> bool:
    return resim.mode in ("RGBA", "LA") or (resim.mode == "P" and "transparency" in resim.info)


def _kok_ad(dosya) -> str:
    return os.path.splitext(os.path.basename(getattr(dosya, "name", "") or "gorsel"))[0] or "gorsel"


def gorsel_dogrula(dosya) -> None:
    _ac(dosya)
    dosya.seek(0)


def kucult(dosya, en_uzun: int = 1920) -> ContentFile:
    """EXIF yönünü uygular, en uzun kenarı sınırlar, EXIF'i atar. Saydam görseller PNG, diğerleri JPEG olur."""
    resim = _ac(dosya)
    resim.thumbnail((en_uzun, en_uzun), Image.LANCZOS)
    tampon = io.BytesIO()
    if _seffaf_mi(resim):
        resim.convert("RGBA").save(tampon, "PNG", optimize=True)
        uzanti = "png"
    else:
        resim.convert("RGB").save(tampon, "JPEG", quality=85, optimize=True, progressive=True)
        uzanti = "jpg"
    return ContentFile(tampon.getvalue(), name=f"{_kok_ad(dosya)}.{uzanti}")


def paylasim_gorseli_uret(dosya) -> ContentFile:
    """1200x630 ortadan kırpılmış, 300 KB altına sıkıştırılmış JPEG üretir."""
    resim = ImageOps.fit(_ac(dosya).convert("RGB"), PAYLASIM_BOYUT, Image.LANCZOS)
    kalite = 85
    while True:
        tampon = io.BytesIO()
        resim.save(tampon, "JPEG", quality=kalite, optimize=True)
        if tampon.tell() < PAYLASIM_UST_SINIR or kalite <= 50:
            break
        kalite -= 5
    return ContentFile(tampon.getvalue(), name=f"{_kok_ad(dosya)}-paylasim.jpg")
