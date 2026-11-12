"""Son inceleme bulgularını sabitleyen testler."""
from datetime import datetime, timezone as dt_tz
from unittest import mock

import pytest

from icerik import og
from icerik.models import Duyuru, Etkinlik
from ortak.html import temiz_html
from ortak.slug import tr_slugify


def test_editor_div_ve_h1_bloklari_korunur():
    sonuc = temiz_html("<h1>Başlık</h1><div>Gövde metni</div><div>İkinci</div><del>eski</del><pre>kod</pre>")
    assert "<h1>Başlık</h1>" in sonuc and "<div>Gövde metni</div>" in sonuc
    assert "<del>eski</del>" in sonuc and "<pre>kod</pre>" in sonuc


def test_alt_cizgi_slug_tireye_doner():
    assert tr_slugify("Burs_2026 Duyurusu") == "burs-2026-duyurusu"


@pytest.mark.django_db
def test_eski_alt_cizgili_slug_og_sayfasi_calisir(client, settings):
    settings.SITE_URL = "https://e.vercel.app"
    og._onbellek.clear()
    d = Duyuru.objects.create(baslik="A")
    Duyuru.objects.filter(pk=d.pk).update(slug="eski_slug")
    with mock.patch("icerik.og._index_cek", return_value="<html><head><title>x</title></head><body></body></html>"):
        assert client.get("/duyurular/eski_slug").status_code == 200


@pytest.mark.django_db
def test_gelecek_tarihli_duyuru_og_404(client, settings):
    from datetime import timedelta
    from django.utils import timezone

    og._onbellek.clear()
    Duyuru.objects.create(baslik="Gelecek", yayin_tarihi=timezone.now() + timedelta(days=3))
    with mock.patch("icerik.og._index_cek", return_value="<html><head></head><body></body></html>"):
        assert client.get("/duyurular/gelecek").status_code == 404


@pytest.mark.django_db
def test_og_etkinlik_tarihi_istanbul_saatiyle(client, settings):
    og._onbellek.clear()
    # 1 Mart 21:30 UTC = 2 Mart 00:30 İstanbul
    Etkinlik.objects.create(baslik="Gece", baslangic=datetime(2026, 3, 1, 21, 30, tzinfo=dt_tz.utc))
    with mock.patch("icerik.og._index_cek", return_value="<html><head></head><body></body></html>"):
        html = client.get("/etkinlikler/gece").content.decode()
    assert "02.03.2026" in html


@pytest.mark.django_db
def test_panel_ingilizce_tarayicida_da_turkce(admin_client):
    sayfa = admin_client.get("/yonetim/", HTTP_ACCEPT_LANGUAGE="en-US,en;q=0.9").content.decode()
    assert "Çıkış" in sayfa or "Oturumu kapat" in sayfa or "Parolayı değiştir" in sayfa


def test_boto3_checksum_ayari_supabase_icin():
    import os

    from django.conf import settings  # noqa: F401  ayarlar yüklensin

    assert os.environ.get("AWS_REQUEST_CHECKSUM_CALCULATION") == "when_required"
    assert os.environ.get("AWS_RESPONSE_CHECKSUM_VALIDATION") == "when_required"
