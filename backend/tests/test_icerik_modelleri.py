import pytest
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile

from icerik.models import Destekci, Dokuman, Duyuru, Etkinlik, SiteAyarlari

pytestmark = pytest.mark.django_db


def test_ayni_baslik_ikinci_kez_ayri_slug():
    a = Duyuru.objects.create(baslik="Burs Duyurusu")
    b = Duyuru.objects.create(baslik="Burs Duyurusu")
    assert (a.slug, b.slug) == ("burs-duyurusu", "burs-duyurusu-2")


def test_slug_baslik_degisince_sabit_kalir():
    d = Duyuru.objects.create(baslik="Eski")
    d.baslik = "Yeni"
    d.save()
    assert d.slug == "eski"


def test_etkinlik_slug_turkce():
    from django.utils import timezone

    e = Etkinlik.objects.create(baslik="İftar Buluşması", baslangic=timezone.now(), tur="bulusma")
    assert e.slug == "iftar-bulusmasi"


def test_duyuru_icerigi_kayitta_temizlenir():
    d = Duyuru.objects.create(baslik="X", icerik="<p>a</p><script>k</script>")
    assert d.icerik == "<p>a</p>"


def test_destekci_varsayilan_izinsiz():
    assert Destekci.objects.create(ad="X", tur="firma").yayin_izni is False


def test_site_ayarlari_tekil():
    assert SiteAyarlari.yukle().pk == SiteAyarlari.yukle().pk == 1
    assert SiteAyarlari.objects.count() == 1


def test_dokuman_4mb_ustu_reddedilir():
    dosya = SimpleUploadedFile("form.pdf", b"0" * (4 * 1024 * 1024 + 1))
    with pytest.raises(ValidationError):
        Dokuman(baslik="F", dosya=dosya).full_clean()


def test_dokuman_yanlis_uzanti_reddedilir():
    with pytest.raises(ValidationError):
        Dokuman(baslik="F", dosya=SimpleUploadedFile("x.exe", b"0")).full_clean()


def test_dokuman_pdf_kabul():
    Dokuman(baslik="F", dosya=SimpleUploadedFile("x.pdf", b"0" * 100)).full_clean()
