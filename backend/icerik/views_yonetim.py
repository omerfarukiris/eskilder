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


KARTLAR = [
    # (başlık, açıklama, simge, admin adres adı, sayaç)
    ("Duyuru ekle", "Burs dönemi, haber ya da önemli bir bilgiyi sitede yayınlayın.", "campaign", "admin:icerik_duyuru_add", None),
    ("Etkinlik / buluşma ekle", "Yaklaşan bir buluşmayı duyurun ya da geçmiş etkinliğin fotoğraflarını ekleyin.", "event", "admin:icerik_etkinlik_add", None),
    ("Gelen mesajlar", "Siteden yazan kişilerin mesajlarını okuyun.", "mail", "admin:iletisim_iletisimmesaji_changelist", "okunmamis"),
    ("Destekçiler", "Bağışçıları ekleyin; sitede görünmeleri için izin kutusunu işaretleyin.", "handshake", "admin:icerik_destekci_changelist", None),
    ("Tüm duyurular", "Yayındaki duyuruları düzenleyin ya da kaldırın.", "list", "admin:icerik_duyuru_changelist", None),
    ("Tüm etkinlikler", "Etkinlikleri düzenleyin, fotoğraf ekleyin.", "calendar_month", "admin:icerik_etkinlik_changelist", None),
    ("Site ayarları", "Telefon, adres, IBAN, Hakkımızda ve Burs sayfası metinleri.", "settings", "admin:icerik_siteayarlari_changelist", None),
    ("Rakamlar, kurul ve belgeler", "Ana sayfadaki rakamlar, yönetim kurulu ve başvuru formları.", "folder_open", "admin:icerik_etkirakami_changelist", None),
]


def ozet(request, context):
    from django.urls import reverse

    okunmamis = okunmamis_sayisi()
    context.update({
        "kartlar": [
            {"baslik": b, "aciklama": a, "simge": i, "adres": reverse(u), "sayi": okunmamis if sayac else None}
            for b, a, i, u, sayac in KARTLAR
        ],
        "okunmamis": okunmamis,
        "son_duyurular": list(Duyuru.objects.all()[:5]),
        "yaklasan_etkinlikler": list(Etkinlik.objects.filter(baslangic__gte=timezone.now()).order_by("baslangic")[:3]),
    })
    return context
