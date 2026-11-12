from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils import timezone

from ortak.html import temiz_html
from ortak.slug import benzersiz_slug

DOKUMAN_UST_SINIR = 4 * 1024 * 1024


def dosya_boyutu_4mb(dosya):
    if dosya and dosya.size > DOKUMAN_UST_SINIR:
        raise ValidationError("Dosya en fazla 4 MB olabilir. Lütfen daha küçük bir dosya yükleyin.")


class SiteAyarlari(models.Model):
    resmi_ad = models.CharField("Resmî dernek adı", max_length=200, blank=True)
    kisa_ad = models.CharField("Kısa ad", max_length=60, blank=True, default="Eskilder")
    slogan = models.CharField("Slogan", max_length=200, blank=True)
    logo = models.ImageField("Logo", upload_to="site/", blank=True, null=True)
    hero_gorsel = models.ImageField("Açılış görseli", upload_to="site/", blank=True, null=True,
                                    help_text="Ana sayfanın en üstündeki büyük fotoğraf. Yatay bir fotoğraf seçin.")
    hero_metin = models.CharField("Açılış metni", max_length=300, blank=True)
    telefon = models.CharField("Telefon", max_length=30, blank=True)
    whatsapp = models.CharField("WhatsApp numarası", max_length=30, blank=True, help_text="Örn: +90 532 000 00 00")
    eposta = models.EmailField("E-posta", blank=True)
    adres = models.TextField("Adres", blank=True)
    harita_embed_url = models.URLField("Harita bağlantısı (embed)", max_length=1000, blank=True,
                                       help_text="Google Haritalar → Paylaş → Harita yerleştir → bağlantıdaki src adresi.")
    iban = models.CharField("IBAN", max_length=40, blank=True)
    hesap_sahibi = models.CharField("Hesap sahibi", max_length=200, blank=True)
    banka = models.CharField("Banka", max_length=100, blank=True)
    destek_ol_metni = models.TextField("Destek Ol metni", blank=True)
    hakkimizda_metni = models.TextField("Hakkımızda metni", blank=True)
    burs_metni = models.TextField("Burs sayfası metni", blank=True)
    kvkk_metni = models.TextField("KVKK aydınlatma metni", blank=True)
    facebook = models.URLField("Facebook", blank=True)
    instagram = models.URLField("Instagram", blank=True)
    x = models.URLField("X (Twitter)", blank=True)
    youtube = models.URLField("YouTube", blank=True)

    class Meta:
        verbose_name = "Site ayarları"
        verbose_name_plural = "Site ayarları"

    def __str__(self):
        return "Site ayarları"

    def save(self, *args, **kwargs):
        self.pk = 1
        for alan in ("hakkimizda_metni", "burs_metni", "kvkk_metni"):
            setattr(self, alan, temiz_html(getattr(self, alan)))
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass

    @classmethod
    def yukle(cls):
        nesne, _ = cls.objects.get_or_create(pk=1)
        return nesne


class SiraliModel(models.Model):
    sira = models.PositiveIntegerField("Sıra", default=0, db_index=True)

    class Meta:
        abstract = True
        ordering = ["sira", "pk"]


class EtkiRakami(SiraliModel):
    etiket = models.CharField("Etiket", max_length=80, help_text="Örn: öğrenciye burs verildi")
    deger = models.CharField("Değer", max_length=20, help_text="Örn: 340+")

    class Meta(SiraliModel.Meta):
        verbose_name = "Etki rakamı"
        verbose_name_plural = "Etki rakamları"

    def __str__(self):
        return f"{self.deger} {self.etiket}"


class SlugluModel(models.Model):
    baslik = models.CharField("Başlık", max_length=200)
    slug = models.SlugField("Adres", max_length=220, unique=True, editable=False)
    kapak = models.ImageField("Kapak görseli", upload_to="kapak/", blank=True, null=True)
    paylasim_gorseli = models.ImageField(upload_to="paylasim/", blank=True, null=True, editable=False)
    yayinda = models.BooleanField("Yayında", default=True)

    ZENGIN_ALAN = None

    class Meta:
        abstract = True

    def __str__(self):
        return self.baslik

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = benzersiz_slug(type(self), self.baslik, haric_pk=self.pk)
        if self.ZENGIN_ALAN:
            setattr(self, self.ZENGIN_ALAN, temiz_html(getattr(self, self.ZENGIN_ALAN)))
        super().save(*args, **kwargs)


class Duyuru(SlugluModel):
    ozet = models.CharField("Özet", max_length=300, blank=True, help_text="Listelerde ve paylaşımlarda görünen kısa açıklama.")
    icerik = models.TextField("İçerik", blank=True)
    yayin_tarihi = models.DateTimeField("Yayın tarihi", default=timezone.now)
    one_cikan = models.BooleanField("Öne çıkan", default=False)

    ZENGIN_ALAN = "icerik"

    class Meta:
        verbose_name = "Duyuru"
        verbose_name_plural = "Duyurular"
        ordering = ["-yayin_tarihi"]


class Etkinlik(SlugluModel):
    TURLER = [("bulusma", "Buluşma"), ("etkinlik", "Etkinlik"), ("burs_toreni", "Burs Töreni"), ("diger", "Diğer")]
    tur = models.CharField("Tür", max_length=20, choices=TURLER, default="bulusma")
    baslangic = models.DateTimeField("Tarih ve saat")
    yer = models.CharField("Yer", max_length=200, blank=True)
    aciklama = models.TextField("Açıklama", blank=True)

    ZENGIN_ALAN = "aciklama"

    class Meta:
        verbose_name = "Etkinlik / Buluşma"
        verbose_name_plural = "Etkinlikler & Buluşmalar"
        ordering = ["-baslangic"]


class FotografModel(SiraliModel):
    gorsel = models.ImageField("Fotoğraf", upload_to="galeri/")
    aciklama = models.CharField("Açıklama", max_length=200, blank=True)

    class Meta(SiraliModel.Meta):
        abstract = True

    def __str__(self):
        return self.aciklama or f"Fotoğraf {self.pk}"


class DuyuruFotografi(FotografModel):
    duyuru = models.ForeignKey(Duyuru, on_delete=models.CASCADE, related_name="fotograflar")

    class Meta(FotografModel.Meta):
        verbose_name = "Fotoğraf"
        verbose_name_plural = "Fotoğraflar"


class EtkinlikFotografi(FotografModel):
    etkinlik = models.ForeignKey(Etkinlik, on_delete=models.CASCADE, related_name="fotograflar")

    class Meta(FotografModel.Meta):
        verbose_name = "Fotoğraf"
        verbose_name_plural = "Fotoğraflar"


class Destekci(SiraliModel):
    TURLER = [("kisi", "Kişi"), ("firma", "Firma")]
    ad = models.CharField("Ad / Firma adı", max_length=200)
    tur = models.CharField("Tür", max_length=10, choices=TURLER, default="kisi")
    logo = models.ImageField("Logo / Fotoğraf", upload_to="destekci/", blank=True, null=True)
    not_metni = models.CharField("Kısa not", max_length=200, blank=True,
                                 help_text="Örn: 2025'te 3 öğrencinin bursunu üstlendi.")
    yayin_izni = models.BooleanField(
        "Sitede yayınlanmasına izin verdi", default=False,
        help_text="İşaretlenmezse bu destekçi sitede GÖRÜNMEZ. Yalnızca izin alınmışsa işaretleyin.",
    )

    class Meta(SiraliModel.Meta):
        verbose_name = "Destekçi"
        verbose_name_plural = "Destekçiler"

    def __str__(self):
        return self.ad


class YonetimKuruluUyesi(SiraliModel):
    ad_soyad = models.CharField("Ad soyad", max_length=120)
    gorev = models.CharField("Görev", max_length=120, help_text="Örn: Başkan")
    fotograf = models.ImageField("Fotoğraf", upload_to="kurul/", blank=True, null=True)

    class Meta(SiraliModel.Meta):
        verbose_name = "Yönetim kurulu üyesi"
        verbose_name_plural = "Yönetim kurulu"

    def __str__(self):
        return f"{self.ad_soyad} ({self.gorev})"


class Dokuman(SiraliModel):
    baslik = models.CharField("Başlık", max_length=200, help_text="Örn: Burs Başvuru Formu 2026")
    dosya = models.FileField(
        "Dosya", upload_to="belge/",
        validators=[FileExtensionValidator(["pdf", "doc", "docx"]), dosya_boyutu_4mb],
        help_text="PDF veya Word dosyası, en fazla 4 MB.",
    )
    yayinda = models.BooleanField("Yayında", default=True)

    class Meta(SiraliModel.Meta):
        verbose_name = "Belge"
        verbose_name_plural = "Belgeler"

    def __str__(self):
        return self.baslik
