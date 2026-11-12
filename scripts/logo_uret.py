"""Eskilder logosunu vektör (SVG) olarak üretir.

Kaynak: derneğin düşük çözünürlüklü logo görüntüsü; şekiller aslına sadık kalınarak yeniden çizildi.
Çıktılar:
  frontend/public/logo.svg          tam logo (dünya, başaklar, kitap, çatı, 1929, ESKİLDER)
  frontend/public/logo-isaret.svg   yalnız amblem (menü ve sekme simgesi için)
"""
import math
from pathlib import Path

KOK = Path(__file__).resolve().parent.parent
YESIL = "#4f9a32"
YESIL_KOYU = "#3d7d24"
ALTIN = "#b39a3c"
BASAK = "#e3b94e"
BASAK_KOYU = "#b88a2a"


def basak(x0, y0, uzunluk, aci, yon):
    """Tek buğday başağı: hafif kavisli sap + iki yana dizili taneler."""
    parcalar = []
    rad = math.radians(aci)
    dx, dy = math.sin(rad), -math.cos(rad)
    nx, ny = -dy, dx
    bukum = 0.12 * yon
    noktalar = []
    for i in range(0, 11):
        t = i / 10
        x = x0 + dx * uzunluk * t + nx * uzunluk * bukum * t * t
        y = y0 + dy * uzunluk * t + ny * uzunluk * bukum * t * t
        noktalar.append((x, y))
    sap = " ".join(f"{x:.1f},{y:.1f}" for x, y in noktalar)
    parcalar.append(f'<polyline points="{sap}" fill="none" stroke="{BASAK_KOYU}" stroke-width="3" stroke-linecap="round"/>')
    for i in range(4, 11):
        t = i / 10
        x, y = noktalar[i]
        kucul = 1 - (i - 4) * 0.07
        for taraf in (-1, 1):
            gx = x + nx * 9 * taraf * kucul
            gy = y + ny * 9 * taraf * kucul
            donus = math.degrees(math.atan2(dy, dx)) + 90 + 28 * taraf
            parcalar.append(
                f'<ellipse cx="{gx:.1f}" cy="{gy:.1f}" rx="{6.5 * kucul:.1f}" ry="{13 * kucul:.1f}" '
                f'transform="rotate({donus:.1f} {gx:.1f} {gy:.1f})" fill="{BASAK}" stroke="{BASAK_KOYU}" stroke-width="1.2"/>'
            )
    ux, uy = noktalar[-1]
    parcalar.append(f'<ellipse cx="{ux + dx * 10:.1f}" cy="{uy + dy * 10:.1f}" rx="5" ry="11" '
                    f'transform="rotate({math.degrees(math.atan2(dy, dx)) + 90:.1f} {ux + dx * 10:.1f} {uy + dy * 10:.1f})" '
                    f'fill="{BASAK}" stroke="{BASAK_KOYU}" stroke-width="1.2"/>')
    return "\n".join(parcalar)


def demet(cx, cy, yon):
    """Üç başaklı demet; yon=-1 sol, +1 sağ."""
    return "\n".join(basak(cx, cy, uzunluk, aci * yon, yon) for uzunluk, aci in ((150, 8), (140, 26), (125, 44)))


def dunya():
    return f"""
  <defs>
    <radialGradient id="okyanus" cx="40%" cy="35%" r="75%">
      <stop offset="0" stop-color="#bfe3f7"/>
      <stop offset=".55" stop-color="#5aa6dd"/>
      <stop offset="1" stop-color="#2a6db3"/>
    </radialGradient>
    <clipPath id="kure"><circle cx="300" cy="190" r="150"/></clipPath>
  </defs>
  <circle cx="300" cy="190" r="150" fill="url(#okyanus)"/>
  <g clip-path="url(#kure)" fill="#6cc04a" stroke="#4f9a32" stroke-width="2">
    <path d="M150 120 C180 90 205 105 200 140 C196 170 215 190 205 225 C196 255 175 270 160 300 L140 300 L140 120 Z"/>
    <path d="M395 70 C420 80 440 110 450 140 L460 140 L460 330 L420 330 C430 300 418 270 425 240 C432 210 410 190 418 160 C424 130 400 110 395 70 Z"/>
    <path d="M330 60 C350 55 372 62 380 75 C368 82 350 80 338 74 Z"/>
  </g>"""


def kitap():
    satirlar = []
    for i in range(3):
        y = 300 + i * 26
        satirlar.append(
            f'<path d="M30 {y + 22} C110 {y - 18} 200 {y - 22} 300 {y + 14} C400 {y - 22} 490 {y - 18} 570 {y + 22}" '
            f'fill="none" stroke="{ALTIN}" stroke-width="15" stroke-linecap="round"/>'
        )
    return "\n  ".join(satirlar)


def cati():
    return (f'<path d="M24 446 L300 392 L576 446 L576 458 L300 410 L24 458 Z" fill="{YESIL}" stroke="{YESIL_KOYU}" stroke-width="2" stroke-linejoin="round"/>\n'
            f'  <rect x="289" y="380" width="22" height="22" fill="#d9c27a" stroke="{YESIL_KOYU}" stroke-width="2"/>\n'
            f'  <text x="300" y="397" text-anchor="middle" font-family="Georgia, serif" font-size="15" font-weight="700" fill="{YESIL_KOYU}">E</text>')


def amblem():
    return f"""{dunya()}
  {demet(262, 300, -1)}
  {demet(338, 300, 1)}
  {kitap()}
  {cati()}"""


def tam_logo():
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 640" role="img" aria-label="Eskilder 1929 logosu">
  <title>Eskilder</title>{amblem()}
  <text x="300" y="472" text-anchor="middle" font-family="Georgia, 'Times New Roman', serif" font-size="46" font-weight="700" fill="#1d1d1d">1929</text>
  <text x="300" y="600" text-anchor="middle" font-family="Arial, Helvetica, sans-serif" font-size="118" fill="{YESIL}" textLength="540" lengthAdjust="spacingAndGlyphs">ESKİLDER</text>
</svg>
"""


def isaret():
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="10 30 580 440" role="img" aria-label="Eskilder amblemi">
  <title>Eskilder</title>{amblem()}
</svg>
"""


if __name__ == "__main__":
    hedef = KOK / "frontend" / "public"
    (hedef / "logo.svg").write_text(tam_logo(), encoding="utf-8")
    (hedef / "logo-isaret.svg").write_text(isaret(), encoding="utf-8")
    print("yazıldı:", hedef / "logo.svg", hedef / "logo-isaret.svg")
