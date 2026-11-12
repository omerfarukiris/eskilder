from django.db import models


class IletisimMesaji(models.Model):
    KONULAR = [("destekci", "Destekçi olmak istiyorum"), ("burs", "Burs hakkında"), ("diger", "Diğer")]
    DURUMLAR = [("yeni", "Yeni"), ("okundu", "Okundu"), ("yanitlandi", "Yanıtlandı")]

    ad_soyad = models.CharField("Ad soyad", max_length=120)
    eposta = models.EmailField("E-posta")
    telefon = models.CharField("Telefon", max_length=30, blank=True)
    konu = models.CharField("Konu", max_length=20, choices=KONULAR)
    mesaj = models.TextField("Mesaj", max_length=5000)
    kvkk_onay = models.BooleanField("KVKK onayı", default=False)
    olusturma = models.DateTimeField("Gönderilme zamanı", auto_now_add=True, db_index=True)
    durum = models.CharField("Durum", max_length=12, choices=DURUMLAR, default="yeni", db_index=True)

    class Meta:
        verbose_name = "Gelen mesaj"
        verbose_name_plural = "Gelen mesajlar"
        ordering = ["-olusturma"]

    def __str__(self):
        return f"{self.ad_soyad} — {self.get_konu_display()}"


class IpKaydi(models.Model):
    """İletişim formu hız sınırı için. 24 saat sonra silinir."""
    ip = models.CharField(max_length=64, db_index=True)
    zaman = models.DateTimeField(auto_now_add=True, db_index=True)
