"""Örnek veriler için kodla çizilen eğitim temalı illüstrasyonlar (telif sorunu yok)."""
import io
import math

from django.core.files.base import ContentFile
from PIL import Image, ImageDraw, ImageFilter

YESIL_KOYU = (20, 51, 38)
YESIL = (31, 77, 58)
YESIL_ACIK = (52, 110, 84)
KREM = (246, 239, 226)
KREM_GOLGE = (226, 214, 192)
ALTIN = (214, 162, 92)
TOPRAK = (178, 120, 63)
KEP = (24, 32, 28)


def _degrade(boyut, bas, son):
    w, h = boyut
    resim = Image.new("RGB", boyut, bas)
    ciz = ImageDraw.Draw(resim)
    for y in range(h):
        for_t = y / h
        renk = tuple(int(bas[i] + (son[i] - bas[i]) * for_t) for i in range(3))
        ciz.line([(0, y), (w, y)], fill=renk)
    return resim


def _isik_halkalari(resim, merkez, s):
    katman = Image.new("RGBA", resim.size, (0, 0, 0, 0))
    ciz = ImageDraw.Draw(katman)
    cx, cy = merkez
    for r, a in ((520, 22), (380, 26), (250, 30)):
        r = int(r * s)
        ciz.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(246, 239, 226, a))
    katman = katman.filter(ImageFilter.GaussianBlur(int(30 * s)))
    resim.paste(katman, (0, 0), katman)


def _yildiz(ciz, x, y, r, renk):
    noktalar = []
    for i in range(8):
        aci = math.pi / 4 * i - math.pi / 2
        rr = r if i % 2 == 0 else r * 0.32
        noktalar.append((x + rr * math.cos(aci), y + rr * math.sin(aci)))
    ciz.polygon(noktalar, fill=renk)


def _kitap(ciz, cx, cy, s):
    """Açık kitap: iki sayfa, ortada sırt, sayfa çizgileri, altında kapak kenarı."""
    gen, yuk, egim = 420 * s, 270 * s, 38 * s
    # kapak (sayfaların altından taşan toprak rengi kenar)
    ciz.polygon([(cx - gen - 22 * s, cy - yuk / 2 + 30 * s), (cx, cy - yuk / 2 + egim + 30 * s),
                 (cx + gen + 22 * s, cy - yuk / 2 + 30 * s), (cx + gen + 22 * s, cy + yuk / 2 + 26 * s),
                 (cx, cy + yuk / 2 + egim + 26 * s), (cx - gen - 22 * s, cy + yuk / 2 + 26 * s)], fill=TOPRAK)
    # sayfa blokları (kalınlık)
    for i in range(4, 0, -1):
        k = i * 5 * s
        ciz.polygon([(cx - gen, cy - yuk / 2 + k), (cx, cy - yuk / 2 + egim + k), (cx, cy + yuk / 2 + egim + k),
                     (cx - gen, cy + yuk / 2 + k)], fill=KREM_GOLGE)
        ciz.polygon([(cx + gen, cy - yuk / 2 + k), (cx, cy - yuk / 2 + egim + k), (cx, cy + yuk / 2 + egim + k),
                     (cx + gen, cy + yuk / 2 + k)], fill=KREM_GOLGE)
    # sayfalar
    ciz.polygon([(cx - gen, cy - yuk / 2), (cx, cy - yuk / 2 + egim), (cx, cy + yuk / 2 + egim), (cx - gen, cy + yuk / 2)], fill=KREM)
    ciz.polygon([(cx + gen, cy - yuk / 2), (cx, cy - yuk / 2 + egim), (cx, cy + yuk / 2 + egim), (cx + gen, cy + yuk / 2)], fill=KREM)
    # sırt
    ciz.line([(cx, cy - yuk / 2 + egim), (cx, cy + yuk / 2 + egim)], fill=KREM_GOLGE, width=int(6 * s))
    # yazı satırları
    for taraf in (-1, 1):
        for i in range(7):
            t = (i + 1) / 9
            y_dis = cy - yuk / 2 + yuk * t + 18 * s
            x1, x2 = cx + taraf * 60 * s, cx + taraf * (gen - 50 * s)
            uzunluk = 1 if i % 3 else 0.72
            x2 = x1 + (x2 - x1) * uzunluk
            y1 = y_dis + egim * (1 - 60 * s / gen)
            y2 = y_dis + egim * (1 - abs(x2 - cx) / gen)
            ciz.line([(x1, y1), (x2, y2)], fill=(200, 188, 166), width=int(7 * s))


def _kep(ciz, cx, cy, s):
    """Mezuniyet kepi: baş kısmı, eşkenar dörtgen tepe, püskül."""
    ciz.polygon([(cx - 150 * s, cy + 20 * s), (cx + 150 * s, cy + 20 * s), (cx + 135 * s, cy + 125 * s),
                 (cx, cy + 150 * s), (cx - 135 * s, cy + 125 * s)], fill=KEP)
    ciz.polygon([(cx, cy - 95 * s), (cx + 300 * s, cy + 15 * s), (cx, cy + 125 * s), (cx - 300 * s, cy + 15 * s)], fill=(34, 44, 39))
    ciz.polygon([(cx, cy - 95 * s), (cx + 300 * s, cy + 15 * s), (cx, cy + 105 * s), (cx - 300 * s, cy + 15 * s)], fill=KEP)
    ciz.ellipse([cx - 16 * s, cy - 4 * s, cx + 16 * s, cy + 28 * s], fill=ALTIN)
    ciz.line([(cx, cy + 12 * s), (cx + 215 * s, cy + 60 * s)], fill=ALTIN, width=int(8 * s))
    ciz.line([(cx + 215 * s, cy + 60 * s), (cx + 215 * s, cy + 190 * s)], fill=ALTIN, width=int(8 * s))
    ciz.polygon([(cx + 197 * s, cy + 185 * s), (cx + 233 * s, cy + 185 * s), (cx + 240 * s, cy + 255 * s),
                 (cx + 190 * s, cy + 255 * s)], fill=ALTIN)


def egitim_gorseli(boyut=(1600, 1000), varyant=0) -> ContentFile:
    """Kitap + kep illüstrasyonu. 2x çizip küçültülür (yumuşak kenarlar)."""
    olcek = 2
    w, h = boyut[0] * olcek, boyut[1] * olcek
    s = min(w / 1600, h / 1000)
    renkler = [(YESIL_KOYU, YESIL_ACIK), ((38, 58, 46), (90, 120, 80)), ((60, 40, 28), TOPRAK)]
    bas, son = renkler[varyant % len(renkler)]
    resim = _degrade((w, h), bas, son)
    cx, cy = w / 2, h * 0.6
    _isik_halkalari(resim, (int(cx), int(cy - 60 * s)), s)
    ciz = ImageDraw.Draw(resim)
    _kitap(ciz, cx, cy, s)
    _kep(ciz, cx - 10 * s, cy - 330 * s, s)
    for (x, y, r) in ((0.18, 0.22, 22), (0.82, 0.18, 16), (0.88, 0.5, 12), (0.12, 0.6, 14), (0.7, 0.1, 9)):
        _yildiz(ciz, w * x, h * y, r * s, (246, 239, 226))
    resim = resim.resize(boyut, Image.LANCZOS)
    tampon = io.BytesIO()
    resim.save(tampon, "JPEG", quality=88, optimize=True)
    return ContentFile(tampon.getvalue(), name="egitim.jpg")
