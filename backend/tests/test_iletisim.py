import json
from datetime import timedelta
from unittest import mock

import pytest
from django.core import mail
from django.utils import timezone

from icerik.models import SiteAyarlari
from iletisim.models import IletisimMesaji, IpKaydi
from iletisim.servis import eski_kayitlari_temizle
from ortak.ip import istemci_ip

pytestmark = pytest.mark.django_db

GECERLI = {"ad_soyad": "Ayşe Yılmaz", "eposta": "ayse@example.com", "telefon": "", "konu": "destekci",
           "mesaj": "Destek olmak istiyorum.", "kvkk_onay": True, "web_sitesi": ""}


def gonder(client, veri=None, ip="1.1.1.1", **ek):
    return client.post("/api/iletisim/", json.dumps({**GECERLI, **(veri or {})}),
                       content_type="application/json", HTTP_X_FORWARDED_FOR=ip, **ek)


def test_gecerli_mesaj_201_ve_kaydedilir(client):
    r = gonder(client)
    assert r.status_code == 201 and r.json() == {"tamam": True}
    m = IletisimMesaji.objects.get()
    assert m.durum == "yeni" and m.konu == "destekci"


def test_kvkk_onaysiz_400(client):
    r = gonder(client, {"kvkk_onay": False})
    assert r.status_code == 400 and "kvkk_onay" in r.json()


def test_gecersiz_eposta_400(client):
    assert "eposta" in gonder(client, {"eposta": "yok"}).json()


def test_bos_mesaj_400(client):
    r = gonder(client, {"mesaj": "  "})
    assert r.status_code == 400 and "mesaj" in r.json()


def test_hata_mesajlari_turkce(client):
    assert "zorunlu" in gonder(client, {"ad_soyad": ""}).json()["ad_soyad"][0].lower()


def test_honeypot_dolu_201_ama_kayit_yok(client):
    assert gonder(client, {"web_sitesi": "http://spam"}).status_code == 201
    assert IletisimMesaji.objects.count() == 0


def test_ayni_ip_altinci_mesaj_429(client):
    for _ in range(5):
        assert gonder(client).status_code == 201
    r = gonder(client)
    assert r.status_code == 429 and "bir saat" in r.json()["hata"]


def test_farkli_x_forwarded_for_ayri_sayilir(client):
    for _ in range(5):
        gonder(client, ip="1.1.1.1, 10.0.0.1")
    assert gonder(client, ip="2.2.2.2").status_code == 201


def test_istemci_ip_oncelik(rf):
    assert istemci_ip(rf.get("/", HTTP_X_FORWARDED_FOR=" 3.3.3.3 , 10.0.0.1")) == "3.3.3.3"
    assert istemci_ip(rf.get("/", HTTP_X_REAL_IP="4.4.4.4")) == "4.4.4.4"
    assert istemci_ip(rf.get("/", REMOTE_ADDR="5.5.5.5")) == "5.5.5.5"


def test_smtp_tanimliysa_bildirim_gider(client, settings):
    settings.EMAIL_HOST = "smtp.example.com"
    settings.EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"
    ayar = SiteAyarlari.yukle()
    ayar.eposta = "dernek@example.com"
    ayar.save()
    gonder(client)
    assert mail.outbox[0].to == ["dernek@example.com"] and "Ayşe Yılmaz" in mail.outbox[0].body


def test_smtp_hata_verse_de_201_ve_kayit_var(client, settings):
    settings.EMAIL_HOST = "smtp.example.com"
    with mock.patch("iletisim.servis.send_mail", side_effect=OSError("smtp kapalı")):
        assert gonder(client).status_code == 201
    assert IletisimMesaji.objects.count() == 1


def test_smtp_tanimsizsa_eposta_gonderilmez(client, settings):
    settings.EMAIL_HOST = ""
    with mock.patch("iletisim.servis.send_mail") as gonderici:
        gonder(client)
    gonderici.assert_not_called()


def test_temizlik_731_gunluk_mesaji_siler_729u_birakir():
    simdi = timezone.now()
    eski = IletisimMesaji.objects.create(ad_soyad="a", eposta="a@a.com", konu="diger", mesaj="m", kvkk_onay=True)
    yeni = IletisimMesaji.objects.create(ad_soyad="b", eposta="b@b.com", konu="diger", mesaj="m", kvkk_onay=True)
    IletisimMesaji.objects.filter(pk=eski.pk).update(olusturma=simdi - timedelta(days=731))
    IletisimMesaji.objects.filter(pk=yeni.pk).update(olusturma=simdi - timedelta(days=729))
    silinen_mesaj, _ = eski_kayitlari_temizle(simdi)
    assert silinen_mesaj == 1 and list(IletisimMesaji.objects.values_list("pk", flat=True)) == [yeni.pk]


def test_temizlik_25_saatlik_ip_siler():
    simdi = timezone.now()
    k = IpKaydi.objects.create(ip="1.1.1.1")
    IpKaydi.objects.create(ip="2.2.2.2")
    IpKaydi.objects.filter(pk=k.pk).update(zaman=simdi - timedelta(hours=25))
    assert eski_kayitlari_temizle(simdi) == (0, 1)


def test_saglik_temizligi_cagirir(client, settings):
    settings.CRON_SECRET = "s"
    k = IpKaydi.objects.create(ip="1.1.1.1")
    IpKaydi.objects.filter(pk=k.pk).update(zaman=timezone.now() - timedelta(hours=30))
    r = client.get("/api/saglik/", HTTP_AUTHORIZATION="Bearer s")
    assert r.json()["silinen_ip"] == 1
