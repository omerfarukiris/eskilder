import pytest
from django.core.management import call_command

from icerik.models import Destekci, Duyuru, EtkiRakami, Etkinlik, SiteAyarlari, YonetimKuruluUyesi


@pytest.fixture(autouse=True)
def medya(tmp_path, settings):
    settings.MEDIA_ROOT = tmp_path


@pytest.mark.django_db
def test_ornek_veri_iki_kez_calisinca_cogalmaz():
    call_command("ornek_veri_yukle")
    call_command("ornek_veri_yukle")
    assert Duyuru.objects.count() == 2 and Destekci.objects.count() == 6
    assert Destekci.objects.filter(yayin_izni=True).count() == 4
    assert EtkiRakami.objects.count() == 4 and YonetimKuruluUyesi.objects.count() == 3
    assert Etkinlik.objects.count() == 2


@pytest.mark.django_db
def test_ornek_veri_gercek_bilgiler_ve_etkinlikler():
    from django.utils import timezone

    call_command("ornek_veri_yukle")
    ayar = SiteAyarlari.yukle()
    assert ayar.eposta == "eskilder68@gmail.com" and "Karatay/Konya" in ayar.adres
    assert "Eskil" in ayar.burs_metni and ayar.kvkk_metni.startswith("<p><strong>Taslak")
    assert Etkinlik.objects.filter(baslangic__gte=timezone.now()).count() == 1
    gecmis = Etkinlik.objects.get(baslangic__lt=timezone.now())
    assert gecmis.fotograflar.count() == 3 and gecmis.kapak
    assert Duyuru.objects.get(slug__startswith="2024-2025").yayin_tarihi.year == 2024
