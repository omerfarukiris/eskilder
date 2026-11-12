from datetime import timedelta

import pytest
from django.utils import timezone

from icerik.models import Destekci, Duyuru, EtkiRakami, Etkinlik, YonetimKuruluUyesi

pytestmark = pytest.mark.django_db


def test_izinsiz_destekci_listede_yok(client):
    Destekci.objects.create(ad="İzinli", yayin_izni=True)
    Destekci.objects.create(ad="İzinsiz", yayin_izni=False)
    r = client.get("/api/destekciler/")
    assert [d["ad"] for d in r.json()] == ["İzinli"]
    assert set(r.json()[0]) == {"ad", "tur", "logo", "not_metni"}


def test_yayinda_olmayan_duyuru_listede_ve_detayda_yok(client):
    Duyuru.objects.create(baslik="Gizli", yayinda=False)
    assert client.get("/api/duyurular/").json()["count"] == 0
    assert client.get("/api/duyurular/gizli/").status_code == 404


def test_gelecek_tarihli_duyuru_detay_404(client):
    Duyuru.objects.create(baslik="İleri", yayin_tarihi=timezone.now() + timedelta(days=1))
    assert client.get("/api/duyurular/ileri/").status_code == 404
    assert client.get("/api/duyurular/").json()["count"] == 0


def test_duyuru_detay_icerik_ve_fotograflar(client):
    Duyuru.objects.create(baslik="Açık", icerik="<p>x</p>")
    veri = client.get("/api/duyurular/acik/").json()
    assert veri["icerik"] == "<p>x</p>" and veri["fotograflar"] == [] and veri["kapak"] is None


def test_duyuru_sayfalama_9(client):
    for i in range(10):
        Duyuru.objects.create(baslik=f"D{i}")
    veri = client.get("/api/duyurular/").json()
    assert veri["count"] == 10 and len(veri["results"]) == 9
    assert len(client.get("/api/duyurular/?sayfa=2").json()["results"]) == 1
    assert set(veri["results"][0]) == {"baslik", "slug", "ozet", "kapak", "yayin_tarihi", "one_cikan"}


def test_etkinlik_yaklasan_gecmis_ayrimi(client):
    simdi = timezone.now()
    Etkinlik.objects.create(baslik="Uzak", baslangic=simdi + timedelta(days=20))
    Etkinlik.objects.create(baslik="Yakın", baslangic=simdi + timedelta(days=2))
    Etkinlik.objects.create(baslik="Eski", baslangic=simdi - timedelta(days=2))
    Etkinlik.objects.create(baslik="Gizli", baslangic=simdi + timedelta(days=1), yayinda=False)
    yak = [e["baslik"] for e in client.get("/api/etkinlikler/?zaman=yaklasan").json()["results"]]
    gec = [e["baslik"] for e in client.get("/api/etkinlikler/?zaman=gecmis").json()["results"]]
    assert yak == ["Yakın", "Uzak"] and gec == ["Eski"]
    ilk = client.get("/api/etkinlikler/?zaman=yaklasan").json()["results"][0]
    assert ilk["tur_adi"] == "Buluşma"
    assert client.get("/api/etkinlikler/gizli/").status_code == 404


def test_ayarlar_rakam_ve_kurul_sirali(client):
    EtkiRakami.objects.create(etiket="b", deger="2", sira=2)
    EtkiRakami.objects.create(etiket="a", deger="1", sira=1)
    YonetimKuruluUyesi.objects.create(ad_soyad="Z", gorev="Üye", sira=5)
    YonetimKuruluUyesi.objects.create(ad_soyad="A", gorev="Başkan", sira=0)
    veri = client.get("/api/ayarlar/").json()
    assert [r["etiket"] for r in veri["rakamlar"]] == ["a", "b"]
    assert [k["ad_soyad"] for k in veri["kurul"]] == ["A", "Z"]
    assert "iban" in veri and veri["dokumanlar"] == []


def test_post_405(client):
    assert client.post("/api/duyurular/", {}).status_code == 405
    assert client.post("/api/ayarlar/", {}).status_code == 405


def test_cache_control(client):
    assert "max-age=60" in client.get("/api/destekciler/")["Cache-Control"]
