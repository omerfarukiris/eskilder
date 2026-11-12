"""Orijinal Eskilder logosunun sadeleştirilmiş, düz (flat) vektör amblemi.

Dünya (üst yarım) + iki buğday başağı + üç altın kitap çizgisi + yeşil çatı.
Küçük boyutta (menü, sekme simgesi) okunaklı kalması için ayrıntı azaltıldı.
"""
import math
from pathlib import Path

ALTIN = "#b8993a"
BASAK = "#e2b54a"
BASAK_KOYU = "#a97f22"
YESIL = "#4f9a32"


def basak(x0, y0, uzunluk, aci_derece, adet=5):
    a = math.radians(aci_derece)
    dx, dy = math.sin(a), -math.cos(a)
    uc_x, uc_y = x0 + dx * uzunluk, y0 + dy * uzunluk
    parca = [f'<line x1="{x0:.1f}" y1="{y0:.1f}" x2="{uc_x:.1f}" y2="{uc_y:.1f}" stroke="{BASAK_KOYU}" stroke-width="1.6" stroke-linecap="round"/>']
    donus = aci_derece
    for i in range(adet):
        t = 0.42 + i * (0.5 / adet)
        cx, cy = x0 + dx * uzunluk * t, y0 + dy * uzunluk * t
        for taraf in (-1, 1):
            gx, gy = cx + math.cos(a) * 3.6 * taraf, cy + math.sin(a) * 3.6 * taraf
            parca.append(f'<ellipse cx="{gx:.1f}" cy="{gy:.1f}" rx="2.6" ry="5" fill="{BASAK}" '
                         f'transform="rotate({donus + 30 * taraf:.1f} {gx:.1f} {gy:.1f})"/>')
    parca.append(f'<ellipse cx="{uc_x:.1f}" cy="{uc_y:.1f}" rx="2.3" ry="4.6" fill="{BASAK}" transform="rotate({donus:.1f} {uc_x:.1f} {uc_y:.1f})"/>')
    return "".join(parca)


def amblem_icerik(on_ek="s"):
    kitap = "".join(
        f'<path d="M8 {78 + i * 7} Q34 {66 + i * 7} 60 {76 + i * 7} Q86 {66 + i * 7} 112 {78 + i * 7}" fill="none" '
        f'stroke="{ALTIN}" stroke-width="4.6" stroke-linecap="round"/>' for i in range(3)
    )
    return f"""<defs>
    <radialGradient id="{on_ek}o" cx="38%" cy="30%" r="80%"><stop offset="0" stop-color="#c3e5f8"/><stop offset=".55" stop-color="#5aa6dd"/><stop offset="1" stop-color="#2b6db2"/></radialGradient>
    <clipPath id="{on_ek}k"><circle cx="60" cy="46" r="34"/></clipPath>
  </defs>
  <g clip-path="url(#{on_ek}k)">
    <rect x="20" y="8" width="80" height="70" fill="url(#{on_ek}o)"/>
    <path d="M24 30 C33 24 38 30 35 39 C32 49 39 55 31 68 L22 68 Z" fill="#6cc04a"/>
    <path d="M82 16 C92 24 96 34 92 44 C88 54 96 60 90 72 L100 72 L100 16 Z" fill="#6cc04a"/>
  </g>
  {basak(56, 74, 46, -24)}{basak(64, 74, 46, 24)}
  {kitap}
  <path d="M8 104 L60 93 L112 104" fill="none" stroke="{YESIL}" stroke-width="5.5" stroke-linejoin="round" stroke-linecap="round"/>"""


def amblem_svg():
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="2 8 116 102" role="img" aria-label="Eskilder amblemi"><title>Eskilder</title>{amblem_icerik()}</svg>\n'


if __name__ == "__main__":
    hedef = Path(__file__).resolve().parent.parent / "frontend" / "public"
    (hedef / "logo-sade.svg").write_text(amblem_svg(), encoding="utf-8")
    print("yazıldı:", hedef / "logo-sade.svg")
