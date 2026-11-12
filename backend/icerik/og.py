"""Duyuru/etkinlik detay adresleri için SPA HTML'ine sayfaya özel meta (Open Graph) etiketleri ekler.

WhatsApp/Facebook botları JavaScript çalıştırmaz; bu yüzden başlık, açıklama ve görsel sunucuda yazılır.
"""
import html
import logging
import re
import time
import urllib.request

from django.conf import settings
from django.http import HttpResponse

from .api import gorunur_duyurular, gorunur_etkinlikler
from .models import SiteAyarlari

log = logging.getLogger(__name__)
ONBELLEK_SURESI = 300
_onbellek: dict = {}

YEDEK_HTML = (
    '<!doctype html><html lang="tr"><head><meta charset="utf-8"><title>Eskilder</title>'
    '<meta name="viewport" content="width=device-width, initial-scale=1"></head>'
    '<body><div id="root"></div><script>location.replace("/")</script></body></html>'
)


def _index_cek(url: str) -> str:
    with urllib.request.urlopen(url, timeout=3) as yanit:  # noqa: S310 — adres ayarlardan gelir
        return yanit.read().decode("utf-8")


def spa_index_html() -> str:
    simdi = time.monotonic()
    kayit = _onbellek.get("index")
    if kayit and simdi - kayit[0] < ONBELLEK_SURESI:
        return kayit[1]
    try:
        icerik = _index_cek(f"{settings.SITE_URL}/index.html")
    except Exception:  # noqa: BLE001 — ağ hatasında son değer ya da yedek kullanılır
        log.warning("SPA index.html çekilemedi", exc_info=True)
        return kayit[1] if kayit else YEDEK_HTML
    _onbellek["index"] = (simdi, icerik)
    return icerik


def meta_ekle(sayfa: str, baslik: str, aciklama: str, gorsel_url, url: str) -> str:
    e = lambda deger: html.escape(deger or "", quote=True)  # noqa: E731
    etiketler = [
        f'<meta name="description" content="{e(aciklama)}">',
        f'<meta property="og:title" content="{e(baslik)}">',
        f'<meta property="og:description" content="{e(aciklama)}">',
        f'<meta property="og:url" content="{e(url)}">',
        '<meta property="og:type" content="article">',
        '<meta property="og:locale" content="tr_TR">',
        '<meta name="twitter:card" content="summary_large_image">',
    ]
    if gorsel_url:
        etiketler.append(f'<meta property="og:image" content="{e(gorsel_url)}">')
        etiketler.append('<meta property="og:image:width" content="1200">')
        etiketler.append('<meta property="og:image:height" content="630">')
    yeni_baslik = f"<title>{e(baslik)} | Eskilder</title>"
    if re.search(r"<title>.*?</title>", sayfa, flags=re.S):
        sayfa = re.sub(r"<title>.*?</title>", lambda _: yeni_baslik, sayfa, count=1, flags=re.S)
    else:
        etiketler.insert(0, yeni_baslik)
    return sayfa.replace("</head>", "\n".join(etiketler) + "\n</head>", 1)


def _mutlak(alan):
    if not alan:
        return None
    url = alan.url
    return url if url.startswith("http") else f"{settings.SITE_URL}{url}"


def _sayfa(request, nesne, aciklama, yol):
    if nesne is None:
        return HttpResponse(spa_index_html(), status=404)
    gorsel = _mutlak(nesne.paylasim_gorseli) or _mutlak(SiteAyarlari.yukle().logo)
    sayfa = meta_ekle(spa_index_html(), nesne.baslik, aciklama, gorsel, f"{settings.SITE_URL}{yol}")
    yanit = HttpResponse(sayfa)
    yanit["Cache-Control"] = "public, max-age=60"
    return yanit


def duyuru_sayfasi(request, slug):
    d = gorunur_duyurular().filter(slug=slug).first()
    return _sayfa(request, d, d.ozet if d else "", f"/duyurular/{slug}")


def etkinlik_sayfasi(request, slug):
    e = gorunur_etkinlikler().filter(slug=slug).first()
    aciklama = ""
    if e:
        aciklama = f"{e.get_tur_display()} · {e.baslangic:%d.%m.%Y}" + (f" · {e.yer}" if e.yer else "")
    return _sayfa(request, e, aciklama, f"/etkinlikler/{slug}")
