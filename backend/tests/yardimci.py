import io
import random

from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image


def gorsel_bayt(boyut=(800, 600), bicim="JPEG", renk=(200, 50, 50), exif_yon=None, gurultu=False, mod="RGB"):
    resim = Image.new(mod, boyut, renk if mod == "RGB" else (*renk, 0))
    if gurultu:
        resim.putdata([tuple(random.randint(0, 255) for _ in range(3)) for _ in range(boyut[0] * boyut[1])])
    tampon = io.BytesIO()
    kw = {}
    if exif_yon:
        exif = Image.Exif()
        exif[0x0112] = exif_yon
        kw["exif"] = exif.tobytes()
    resim.save(tampon, bicim, **kw)
    return tampon.getvalue()


def yukleme(ad="foto.jpg", **kw):
    bicim = "PNG" if ad.endswith(".png") else "JPEG"
    return SimpleUploadedFile(ad, gorsel_bayt(bicim=bicim, **kw), content_type=f"image/{bicim.lower()}")
