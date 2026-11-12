from django.conf import settings
from django.http import HttpResponse
from django.utils.html import escape

from .api import gorunur_duyurular, gorunur_etkinlikler

STATIK_SAYFALAR = ["/", "/hakkimizda", "/burs", "/duyurular", "/etkinlikler", "/destekcilerimiz", "/destek-ol", "/iletisim"]


def sitemap(request):
    adresler = [(yol, None) for yol in STATIK_SAYFALAR]
    adresler += [(f"/duyurular/{d.slug}", d.yayin_tarihi) for d in gorunur_duyurular()]
    adresler += [(f"/etkinlikler/{e.slug}", None) for e in gorunur_etkinlikler()]
    satirlar = []
    for yol, tarih in adresler:
        lastmod = f"<lastmod>{tarih:%Y-%m-%d}</lastmod>" if tarih else ""
        satirlar.append(f"<url><loc>{escape(settings.SITE_URL + yol)}</loc>{lastmod}</url>")
    xml = ('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
           + "\n".join(satirlar) + "\n</urlset>\n")
    return HttpResponse(xml, content_type="application/xml")


def robots(request):
    metin = f"User-agent: *\nDisallow: /yonetim/\nDisallow: /api/\nSitemap: {settings.SITE_URL}/sitemap.xml\n"
    return HttpResponse(metin, content_type="text/plain")
