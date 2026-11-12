"""Yönetim paneli özet ekranı ve kenar menüsü yardımcıları."""
from django.utils import timezone

from iletisim.models import IletisimMesaji

from .models import Duyuru, Etkinlik


def okunmamis_sayisi() -> int:
    return IletisimMesaji.objects.filter(durum="yeni").count()


def okunmamis_mesaj_rozeti(request):
    sayi = okunmamis_sayisi()
    return sayi or None


def sadece_super(request) -> bool:
    return bool(request.user and request.user.is_superuser)


def ozet(request, context):
    context.update({
        "okunmamis": okunmamis_sayisi(),
        "son_duyurular": list(Duyuru.objects.all()[:5]),
        "yaklasan_etkinlikler": list(Etkinlik.objects.filter(baslangic__gte=timezone.now()).order_by("baslangic")[:3]),
    })
    return context
