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


@pytest.mark.django_db
def test_hakkimizda_ornek_notu_yok_ve_yeni_alinti():
    call_command("ornek_veri_yukle")
    metin = SiteAyarlari.yukle().hakkimizda_metni
    assert "Örnek metin" not in metin and "panelden" not in metin
    assert "sadaka-i câriye" in metin and "Vasiyyet 14" in metin and "lise ve üniversite" in metin


@pytest.mark.django_db
def test_burs_duyurulari_egitim_gorselli():
    from PIL import Image

    call_command("ornek_veri_yukle")
    for d in Duyuru.objects.all():
        assert d.kapak.name.split("/")[-1].startswith("egitim")
        assert Image.open(d.kapak.path).size == (1600, 1000)


@pytest.mark.django_db
def test_sadece_bossa_secenegi_dolu_veritabanina_dokunmaz():
    call_command("ornek_veri_yukle")
    Destekci.objects.filter(ad__startswith="Örnek İzinsiz").delete()
    call_command("ornek_veri_yukle", "--sadece-bossa")
    assert Destekci.objects.count() == 4


@pytest.mark.django_db
def test_sadece_bossa_secenegi_bos_veritabanini_doldurur():
    call_command("ornek_veri_yukle", "--sadece-bossa")
    assert Duyuru.objects.count() == 2
