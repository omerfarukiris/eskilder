import logging
from datetime import timedelta

from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone

from icerik.models import SiteAyarlari

from .models import IletisimMesaji, IpKaydi

log = logging.getLogger(__name__)

SAATLIK_SINIR = 5
MESAJ_SAKLAMA = timedelta(days=730)
IP_SAKLAMA = timedelta(hours=24)


def sinir_asildi_mi(ip: str) -> bool:
    """Son bir saatte bu IP'den SAATLIK_SINIR veya daha fazla deneme varsa True; değilse denemeyi kaydeder."""
    if IpKaydi.objects.filter(ip=ip, zaman__gte=timezone.now() - timedelta(hours=1)).count() >= SAATLIK_SINIR:
        return True
    IpKaydi.objects.create(ip=ip)
    return False


def bildirim_gonder(mesaj: IletisimMesaji) -> bool:
    if not settings.EMAIL_HOST:
        return False
    alici = SiteAyarlari.yukle().eposta
    if not alici:
        return False
    govde = (
        f"Siteden yeni mesaj var.\n\nAd soyad: {mesaj.ad_soyad}\nE-posta: {mesaj.eposta}\n"
        f"Telefon: {mesaj.telefon or '-'}\nKonu: {mesaj.get_konu_display()}\n\n{mesaj.mesaj}\n"
    )
    try:
        send_mail(f"[Eskilder] Yeni mesaj: {mesaj.get_konu_display()}", govde, None, [alici])
    except Exception:  # noqa: BLE001 — gönderim hatası mesajı kaybettirmemeli
        log.exception("İletişim bildirimi gönderilemedi (mesaj %s)", mesaj.pk)
        return False
    return True


def eski_kayitlari_temizle(simdi=None) -> tuple[int, int]:
    simdi = simdi or timezone.now()
    silinen_mesaj, _ = IletisimMesaji.objects.filter(olusturma__lt=simdi - MESAJ_SAKLAMA).delete()
    silinen_ip, _ = IpKaydi.objects.filter(zaman__lt=simdi - IP_SAKLAMA).delete()
    return silinen_mesaj, silinen_ip
