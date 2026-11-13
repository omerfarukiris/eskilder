"""YONETICI_KULLANICI ve YONETICI_SIFRE ortam değişkenleri tanımlıysa ilk süper yöneticiyi oluşturur.

Vercel derlemesinde çalışır. Kullanıcı zaten varsa hiçbir şey değiştirmez (panelden değiştirilen şifre korunur).
"""
import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Ortam değişkenlerinden ilk yönetici hesabını oluşturur (varsa dokunmaz)."

    def handle(self, *args, **opts):
        kullanici = os.environ.get("YONETICI_KULLANICI", "").strip()
        sifre = os.environ.get("YONETICI_SIFRE", "")
        if not kullanici or not sifre:
            self.stdout.write("YONETICI_KULLANICI/YONETICI_SIFRE tanımlı değil, atlandı.")
            return
        Kullanici = get_user_model()
        if Kullanici.objects.filter(username=kullanici).exists():
            self.stdout.write(f"'{kullanici}' zaten var, değiştirilmedi.")
            return
        Kullanici.objects.create_superuser(username=kullanici, email="", password=sifre)
        self.stdout.write(self.style.SUCCESS(f"Yönetici '{kullanici}' oluşturuldu."))
