import pytest
from django.contrib.auth.models import User
from django.core.management import call_command

pytestmark = pytest.mark.django_db


def test_ortam_degiskeni_yoksa_bir_sey_yapmaz(monkeypatch):
    monkeypatch.delenv("YONETICI_KULLANICI", raising=False)
    monkeypatch.delenv("YONETICI_SIFRE", raising=False)
    call_command("yonetici_olustur")
    assert User.objects.count() == 0


def test_yoksa_super_kullanici_olusturur(monkeypatch):
    monkeypatch.setenv("YONETICI_KULLANICI", "eskilder")
    monkeypatch.setenv("YONETICI_SIFRE", "Gizli-Sifre-2026")
    call_command("yonetici_olustur")
    k = User.objects.get(username="eskilder")
    assert k.is_superuser and k.is_staff and k.check_password("Gizli-Sifre-2026")


def test_varsa_sifreyi_degistirmez(monkeypatch):
    User.objects.create_superuser("eskilder", password="Ilk-Sifre-123")
    monkeypatch.setenv("YONETICI_KULLANICI", "eskilder")
    monkeypatch.setenv("YONETICI_SIFRE", "Baska-Sifre-456")
    call_command("yonetici_olustur")
    assert User.objects.get(username="eskilder").check_password("Ilk-Sifre-123")
