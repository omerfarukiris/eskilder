from datetime import timedelta
from unittest import mock

import pytest
from django.utils import timezone

from icerik import og
from icerik.models import Duyuru, Etkinlik
from tests.yardimci import yukleme

pytestmark = pytest.mark.django_db

SPA = '<!doctype html><html><head><title>Eskilder</title><script src="/assets/i-abc.js"></script></head><body><div id="root"></div></body></html>'


@pytest.fixture(autouse=True)
def ortam(settings, tmp_path):
    settings.MEDIA_ROOT = tmp_path
    settings.SITE_URL = "https://eskilder.vercel.app"
    og._onbellek.clear()
    with mock.patch("icerik.og._index_cek", return_value=SPA) as cek:
        yield cek


def test_duyuru_og_etiketleri(client):
    Duyuru.objects.create(baslik="Burs Başladı", ozet="Başvurular açık", kapak=yukleme())
    r = client.get("/duyurular/burs-basladi")
    html = r.content.decode()
    assert r.status_code == 200 and "<title>Burs Başladı | Eskilder</title>" in html
    assert '<meta property="og:title" content="Burs Başladı">' in html
    assert '<meta name="description" content="Başvurular açık">' in html
    assert 'property="og:image" content="https://' in html and "paylasim" in html
    assert '<meta property="og:url" content="https://eskilder.vercel.app/duyurular/burs-basladi">' in html
    assert '/assets/i-abc.js' in html and html.count("<title>") == 1


def test_sonda_egik_cizgi_de_calisir(client):
    Duyuru.objects.create(baslik="A")
    assert client.get("/duyurular/a/").status_code == 200


def test_baslikta_tirnak_kacislanir(client):
    Duyuru.objects.create(baslik='Ali "Usta" <b>', ozet="")
    html = client.get("/duyurular/ali-usta-b").content.decode()
    assert "&quot;Usta&quot;" in html and "<b>" not in html.split("</head>")[0].split("<title>")[1]


def test_yayinda_olmayan_duyuru_og_404(client):
    Duyuru.objects.create(baslik="Gizli", yayinda=False)
    Duyuru.objects.create(baslik="İleri", yayin_tarihi=timezone.now() + timedelta(days=2))
    for adres in ("/duyurular/gizli", "/duyurular/ileri", "/duyurular/yok-boyle"):
        r = client.get(adres)
        assert r.status_code == 404 and 'id="root"' in r.content.decode()


def test_etkinlik_og_kapaksizsa_logo_yoksa_imaj_yok(client):
    Etkinlik.objects.create(baslik="Buluşma", baslangic=timezone.now())
    html = client.get("/etkinlikler/bulusma").content.decode()
    assert '<meta property="og:title" content="Buluşma">' in html and "og:image" not in html


def test_index_cekilemezse_yedek_html_200(client, ortam):
    ortam.side_effect = OSError("ağ yok")
    Duyuru.objects.create(baslik="A")
    r = client.get("/duyurular/a")
    assert r.status_code == 200 and 'id="root"' in r.content.decode()


def test_index_onbellege_alinir(client, ortam):
    Duyuru.objects.create(baslik="A")
    client.get("/duyurular/a")
    client.get("/duyurular/a")
    assert ortam.call_count == 1


def test_sitemap_yayindakileri_icerir_taslagi_icermez(client):
    Duyuru.objects.create(baslik="Açık")
    Duyuru.objects.create(baslik="Taslak", yayinda=False)
    xml = client.get("/sitemap.xml").content.decode()
    assert "https://eskilder.vercel.app/duyurular/acik" in xml and "taslak" not in xml
    assert "https://eskilder.vercel.app/destek-ol" in xml


def test_robots_yonetimi_engeller(client):
    metin = client.get("/robots.txt").content.decode()
    assert "Disallow: /yonetim/" in metin and "Sitemap: https://eskilder.vercel.app/sitemap.xml" in metin
