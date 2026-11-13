import pytest
from django.contrib.auth.models import Group, User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import RequestFactory

from icerik.models import Duyuru, Etkinlik, SiteAyarlari
from icerik.views_yonetim import okunmamis_mesaj_rozeti, ozet
from iletisim.models import IletisimMesaji
from tests.yardimci import yukleme

pytestmark = pytest.mark.django_db


@pytest.fixture(autouse=True)
def medya(tmp_path, settings):
    settings.MEDIA_ROOT = tmp_path


@pytest.fixture
def editor(client):
    k = User.objects.create_user("editor", password="x-Guclu-Sifre-1", is_staff=True)
    k.groups.add(Group.objects.get(name="Editör"))
    client.force_login(k)
    return client


def mesaj(**kw):
    return IletisimMesaji.objects.create(ad_soyad="A", eposta="a@a.com", konu="diger", mesaj="m", kvkk_onay=True, **kw)


def test_editor_grubu_migrationla_olusur():
    izinler = set(Group.objects.get(name="Editör").permissions.values_list("codename", flat=True))
    assert {"add_duyuru", "change_destekci", "change_iletisimmesaji", "view_siteayarlari"} <= izinler
    assert not any(i.endswith("_user") or i.endswith("_group") for i in izinler)


def test_editor_kullanicilara_erisemez(editor):
    assert editor.get("/yonetim/auth/user/").status_code == 403


def test_panel_turkce(editor):
    assert "Eskilder Yönetim" in editor.get("/yonetim/").content.decode()


def test_editor_duyuru_ekleyebilir(editor):
    r = editor.post("/yonetim/icerik/duyuru/add/", {
        "baslik": "Yeni Duyuru", "ozet": "", "icerik": "<p>x</p>", "yayin_tarihi_0": "2026-11-13",
        "yayin_tarihi_1": "10:00:00", "yayinda": "on",
        "fotograflar-TOTAL_FORMS": "0", "fotograflar-INITIAL_FORMS": "0",
        "fotograflar-MIN_NUM_FORMS": "0", "fotograflar-MAX_NUM_FORMS": "1000",
    })
    assert r.status_code == 302, r.content.decode()[:2000]
    assert Duyuru.objects.get().slug == "yeni-duyuru"


def test_mesaj_acilinca_okundu_olur(editor):
    m = mesaj()
    assert editor.get(f"/yonetim/iletisim/iletisimmesaji/{m.pk}/change/").status_code == 200
    m.refresh_from_db()
    assert m.durum == "okundu"


def test_mesaj_eklenemez(editor):
    assert editor.get("/yonetim/iletisim/iletisimmesaji/add/").status_code == 403


def test_site_ayarlari_listesi_tekil_kayda_yonlenir(editor):
    r = editor.get("/yonetim/icerik/siteayarlari/")
    assert r.status_code == 302 and r["Location"].endswith(f"/yonetim/icerik/siteayarlari/{SiteAyarlari.yukle().pk}/change/")


def test_galeri_yukle_staff_olmayan_reddedilir(client):
    d = Duyuru.objects.create(baslik="D")
    k = User.objects.create_user("normal", password="x")
    client.force_login(k)
    r = client.post(f"/yonetim/icerik/duyuru/{d.pk}/galeri-yukle/", {"dosya": yukleme()})
    assert r.status_code in (302, 403) and d.fotograflar.count() == 0


def test_galeri_yukle_gorsel_ekler(editor):
    e = Etkinlik.objects.create(baslik="E", baslangic="2026-01-01T10:00:00Z")
    r = editor.post(f"/yonetim/icerik/etkinlik/{e.pk}/galeri-yukle/", {"dosya": yukleme(boyut=(3000, 2000))})
    assert r.status_code == 200 and "gorsel" in r.json()
    assert e.fotograflar.count() == 1


def test_galeri_yukle_bozuk_dosya_400_turkce_mesaj(editor):
    d = Duyuru.objects.create(baslik="D")
    r = editor.post(f"/yonetim/icerik/duyuru/{d.pk}/galeri-yukle/", {"dosya": SimpleUploadedFile("a.heic", b"xx")})
    assert r.status_code == 400 and "desteklenmiyor" in r.json()["hata"]


def test_ozet_okunmamis_sayisi():
    mesaj()
    mesaj()
    mesaj(durum="okundu")
    istek = RequestFactory().get("/")
    assert ozet(istek, {})["okunmamis"] == 2
    assert okunmamis_mesaj_rozeti(istek) == 2


def test_rozet_sifirsa_bos():
    assert okunmamis_mesaj_rozeti(RequestFactory().get("/")) is None


def test_destekci_listesinde_izin_sutunu(editor):
    from icerik.models import Destekci

    Destekci.objects.create(ad="Firma X", yayin_izni=False)
    sayfa = editor.get("/yonetim/icerik/destekci/").content.decode()
    assert "Firma X" in sayfa and "yayin_izni" in sayfa


def test_ozet_ekrani_sade_yonlendirme_kartlari(editor):
    sayfa = editor.get("/yonetim/").content.decode()
    assert "Ne yapmak istiyorsunuz?" in sayfa
    for adres in ("/yonetim/icerik/duyuru/add/", "/yonetim/icerik/etkinlik/add/", "/yonetim/icerik/destekci/",
                  "/yonetim/iletisim/iletisimmesaji/", "/yonetim/icerik/siteayarlari/"):
        assert adres in sayfa


def test_panel_acik_temada(settings):
    assert settings.UNFOLD["THEME"] == "light"
