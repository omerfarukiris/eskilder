import io

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image

from icerik.models import Destekci, Duyuru
from ortak.gorsel import GorselHatasi, kucult, paylasim_gorseli_uret
from tests.yardimci import gorsel_bayt, yukleme


def ac(icerik):
    icerik.seek(0)
    return Image.open(io.BytesIO(icerik.read()))


def test_kucult_en_uzun_kenar_1920():
    sonuc = kucult(yukleme(boyut=(4000, 3000)))
    assert ac(sonuc).size == (1920, 1440)


def test_kucult_kucuk_gorseli_buyutmez():
    assert ac(kucult(yukleme(boyut=(640, 480)))).size == (640, 480)


def test_kucult_exif_yonu_uygulanir_ve_exif_silinir():
    resim = ac(kucult(yukleme(boyut=(100, 50), exif_yon=6)))
    assert resim.size == (50, 100)
    assert 0x0112 not in resim.getexif()


def test_kucult_seffaf_png_png_kalir():
    sonuc = kucult(yukleme("logo.png", mod="RGBA"))
    assert ac(sonuc).format == "PNG" and sonuc.name.endswith(".png")


def test_paylasim_gorseli_boyut_ve_agirlik():
    sonuc = paylasim_gorseli_uret(yukleme(boyut=(1500, 1000), gurultu=True))
    assert ac(sonuc).size == (1200, 630)
    assert sonuc.size < 300 * 1024


def test_bozuk_dosya_gorsel_hatasi():
    with pytest.raises(GorselHatasi) as hata:
        kucult(SimpleUploadedFile("foto.heic", b"HEIC degil"))
    assert "desteklenmiyor" in str(hata.value)


@pytest.mark.django_db
def test_kapak_yuklenince_kucultulur_ve_paylasim_gorseli_olusur(tmp_path, settings):
    settings.MEDIA_ROOT = tmp_path
    d = Duyuru.objects.create(baslik="Kapak", kapak=yukleme(boyut=(3000, 2000)))
    assert Image.open(d.kapak.path).size == (1920, 1280)
    assert Image.open(d.paylasim_gorseli.path).size == (1200, 630)


@pytest.mark.django_db
def test_kapak_degismeden_kaydedince_tekrar_islenmez(tmp_path, settings):
    settings.MEDIA_ROOT = tmp_path
    d = Duyuru.objects.create(baslik="Kapak", kapak=yukleme())
    ad = d.paylasim_gorseli.name
    d.baslik = "Yeni"
    d.save()
    assert d.paylasim_gorseli.name == ad


@pytest.mark.django_db
def test_kapak_kaldirilinca_paylasim_gorseli_silinir(tmp_path, settings):
    settings.MEDIA_ROOT = tmp_path
    d = Duyuru.objects.create(baslik="Kapak", kapak=yukleme())
    d.kapak = None
    d.save()
    assert not d.paylasim_gorseli


@pytest.mark.django_db
def test_destekci_logosu_kucultulur(tmp_path, settings):
    settings.MEDIA_ROOT = tmp_path
    s = Destekci.objects.create(ad="F", logo=yukleme(boyut=(2500, 500)))
    assert Image.open(s.logo.path).size == (1920, 384)
