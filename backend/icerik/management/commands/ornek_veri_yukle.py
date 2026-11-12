"""Deneme sürümü için örnek veri: eski siteden gerçek bilgiler + panelden değiştirilebilir yer tutucular.

İki kez çalıştırıldığında kayıtları çoğaltmaz.
"""
import io
from datetime import datetime, timedelta

from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone
from PIL import Image, ImageDraw

from icerik.models import (
    Destekci, Duyuru, EtkiRakami, Etkinlik, EtkinlikFotografi, SiteAyarlari, YonetimKuruluUyesi,
)

RENKLER = [((31, 77, 58), (178, 120, 63)), ((52, 92, 70), (214, 170, 98)), ((90, 60, 40), (31, 77, 58))]

BURS_METNI = """
<h2>Kimler başvurabilir?</h2>
<ul>
<li>Nüfusu Aksaray'ın Eskil ilçesine kayıtlı olan,</li>
<li>Bir lisede ya da üniversitede (ön lisans veya lisans) öğrenimine devam eden öğrenciler.</li>
</ul>
<h2>Burs koşulları</h2>
<ul>
<li>Bursumuz karşılıksızdır, geri ödeme istenmez.</li>
<li>Ödemeler her ayın 25'i ile 30'u arasında öğrencinin kendi banka hesabına yapılır.</li>
</ul>
<h2>Nasıl başvurulur?</h2>
<p>Aşağıdaki başvuru formunu indirip doldurun, fotoğrafınızı ekleyip imzalayın ve istenen belgelerle birlikte
kargo ya da PTT ile dernek adresimize gönderin. Başvuru tarihleri her dönem Duyurular sayfasında ilan edilir.</p>
"""

HAKKIMIZDA = """
<p><strong>Örnek metin — panelden değiştirin.</strong> Eskilder, Aksaray'ın Eskil ilçesinden yetişen gençlerin
lise ve üniversite eğitimlerini desteklemek için bir araya gelen Eskillilerin kurduğu bir dernektir.</p>
<p>Gelirimizin tamamı, memleketine gönül vermiş Eskilli iş insanlarının ve hayırseverlerin bağışlarından oluşur.
Her yıl başvuruları değerlendirip ihtiyaç sahibi öğrencilerimize karşılıksız burs veriyoruz.</p>
<blockquote>Memleketlinin memleketliye desteği.</blockquote>
"""

KVKK = """
<p><strong>Taslak — dernek tarafından kontrol edilmelidir.</strong></p>
<h2>Kişisel verilerin korunması hakkında aydınlatma metni</h2>
<p>6698 sayılı Kişisel Verilerin Korunması Kanunu uyarınca, iletişim formu aracılığıyla paylaştığınız ad soyad,
e-posta, telefon ve mesaj bilgileriniz yalnızca talebinize dönüş yapmak amacıyla derneğimiz tarafından işlenir.</p>
<p>Bu bilgiler üçüncü kişilerle paylaşılmaz ve en fazla 2 yıl saklandıktan sonra silinir. Kötüye kullanımı önlemek
için IP adresiniz 24 saat süreyle tutulur.</p>
<p>Kanunun 11. maddesindeki haklarınızı kullanmak için bize e-posta ile ulaşabilirsiniz.</p>
"""

DUYURULAR = [
    {
        "baslik": "2024-2025 Eğitim Öğretim Dönemi Burs Başvuruları Başladı",
        "ozet": "2024-2025 dönemi burs başvuruları 23 Aralık 2024 – 10 Ocak 2025 tarihleri arasında alınmıştır.",
        "tarih": datetime(2024, 12, 23, 10, 0),
        "icerik": "<p>2024-2025 eğitim öğretim dönemi burs başvurularımız 23 Aralık 2024 Pazartesi günü başlamış, "
                  "10 Ocak 2025 Cuma günü sona ermiştir.</p><p>Başvuru koşulları ve gerekli belgeler için "
                  "Burs sayfamızı inceleyebilirsiniz.</p>",
    },
    {
        "baslik": "2023-2024 Eğitim Öğretim Yılı İçin Burs Başvurularını Başlatıyoruz",
        "ozet": "2023-2024 dönemi burs başvuruları 8 Kasım – 8 Aralık 2023 tarihleri arasında alınmıştır.",
        "tarih": datetime(2023, 11, 8, 10, 0),
        "icerik": "<p>2023-2024 eğitim öğretim yılı burs başvurularımız 8 Kasım 2023 Çarşamba günü başlamış, "
                  "8 Aralık 2023 Cuma günü sona ermiştir.</p>",
    },
]

RAKAMLAR = [("Örnek: kuruluş yılı", "2012"), ("Örnek: öğrenciye burs", "340+"),
            ("Örnek: destekçi iş insanı", "60+"), ("Örnek: mezun bursiyer", "120+")]

DESTEKCILER = [
    ("Örnek Yapı A.Ş.", "firma", True, "Örnek: 2025'te 3 öğrencinin bursunu üstlendi."),
    ("Örnek Gıda Ltd.", "firma", True, ""),
    ("Örnek Lojistik", "firma", True, ""),
    ("Örnek Ahmet Yılmaz", "kisi", True, "Örnek: kurucu destekçi"),
    ("Örnek İzinsiz Firma", "firma", False, "Yayın izni yok — sitede görünmez."),
    ("Örnek İzinsiz Kişi", "kisi", False, "Yayın izni yok — sitede görünmez."),
]

KURUL = [("Örnek Ad Soyad", "Başkan"), ("Örnek Ad Soyad 2", "Başkan Yardımcısı"), ("Örnek Ad Soyad 3", "Sayman")]


def yer_tutucu(metin: str, boyut=(1600, 900), renk_index=0) -> ContentFile:
    """Yazısız, markalı degrade yer tutucu görsel (metin yalnızca dosya adı tohumu olarak kullanılır)."""
    bas, son = RENKLER[renk_index % len(RENKLER)]
    resim = Image.new("RGB", boyut, bas)
    ciz = ImageDraw.Draw(resim, "RGBA")
    for x in range(boyut[0]):
        t = x / boyut[0]
        ciz.line([(x, 0), (x, boyut[1])], fill=tuple(int(bas[i] + (son[i] - bas[i]) * t) for i in range(3)))
    w, h = boyut
    tohum = sum(map(ord, metin))
    for i in range(5):
        r = int(h * (0.25 + ((tohum + i * 37) % 40) / 100))
        cx = int(w * (((tohum * (i + 3)) % 100) / 100))
        cy = int(h * (((tohum * (i + 7)) % 100) / 100))
        ciz.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 250, 240, 18))
    tampon = io.BytesIO()
    resim.save(tampon, "JPEG", quality=85)
    return ContentFile(tampon.getvalue(), name="ornek.jpg")


def yerel(dt: datetime):
    return timezone.make_aware(dt)


class Command(BaseCommand):
    help = "Deneme sürümü için örnek içerik yükler (tekrar çalıştırılabilir)."

    @transaction.atomic
    def handle(self, *args, **opts):
        ayar = SiteAyarlari.yukle()
        if not ayar.resmi_ad:
            ayar.resmi_ad = "Eskil Kültür Eğitim ve Dayanışma Derneği"
            ayar.kisa_ad = "Eskilder"
            ayar.slogan = "Eskil'in çocukları için"
            ayar.hero_metin = "Eskil'den yetişen gençlerin lise ve üniversite yolculuğunda, memleketlileri olarak yanlarındayız."
            ayar.eposta = "eskilder68@gmail.com"
            ayar.adres = "Çelebi Mah. Şehit Battal Yıldız Sk. Derinpark Sitesi No: 1/CF Karatay/Konya"
            ayar.telefon = "0 (332) 000 00 00"
            ayar.whatsapp = "+90 500 000 00 00"
            ayar.iban = "TR00 0000 0000 0000 0000 0000 00"
            ayar.hesap_sahibi = "Örnek: Eskilder Derneği"
            ayar.banka = "Örnek Banka"
            ayar.destek_ol_metni = ("Bağışlarınız doğrudan Eskilli öğrencilerimizin burslarına dönüşüyor. "
                                    "Bir öğrencinin bir yıllık bursunu üstlenerek onun hayatına dokunabilirsiniz.")
            ayar.hakkimizda_metni = HAKKIMIZDA.strip()
            ayar.burs_metni = BURS_METNI.strip()
            ayar.kvkk_metni = KVKK.strip()
            ayar.hero_gorsel = yer_tutucu("Örnek açılış fotoğrafı — Eskil", (1920, 1080))
            ayar.save()

        for d in DUYURULAR:
            if not Duyuru.objects.filter(baslik=d["baslik"]).exists():
                Duyuru.objects.create(baslik=d["baslik"], ozet=d["ozet"], icerik=d["icerik"],
                                      yayin_tarihi=yerel(d["tarih"]), kapak=yer_tutucu("Burs Başvuruları", renk_index=1))

        for i, (etiket, deger) in enumerate(RAKAMLAR):
            EtkiRakami.objects.get_or_create(etiket=etiket, defaults={"deger": deger, "sira": i})

        for i, (ad, tur, izin, not_metni) in enumerate(DESTEKCILER):
            Destekci.objects.get_or_create(ad=ad, defaults={"tur": tur, "yayin_izni": izin, "not_metni": not_metni, "sira": i})

        for i, (ad, gorev) in enumerate(KURUL):
            YonetimKuruluUyesi.objects.get_or_create(ad_soyad=ad, defaults={"gorev": gorev, "sira": i})

        simdi = timezone.localtime()
        if not Etkinlik.objects.filter(baslik="Örnek: Geleneksel Eskilliler Buluşması").exists():
            Etkinlik.objects.create(
                baslik="Örnek: Geleneksel Eskilliler Buluşması", tur="bulusma",
                baslangic=(simdi + timedelta(days=30)).replace(hour=19, minute=0, second=0, microsecond=0),
                yer="Örnek: Konya", aciklama="<p>Örnek açıklama: Eskilli iş insanları, öğrencilerimiz ve "
                                              "ailelerini yıllık buluşmamızda bir araya getiriyoruz.</p>",
                kapak=yer_tutucu("Eskilliler Buluşması", renk_index=2),
            )
        if not Etkinlik.objects.filter(baslik="Örnek: Bursiyerlerle İftar Buluşması").exists():
            gecmis = Etkinlik.objects.create(
                baslik="Örnek: Bursiyerlerle İftar Buluşması", tur="bulusma",
                baslangic=(simdi - timedelta(days=200)).replace(hour=19, minute=0, second=0, microsecond=0),
                yer="Örnek: Eskil", aciklama="<p>Örnek açıklama: Bursiyer öğrencilerimiz ve destekçilerimizle "
                                             "iftar sofrasında buluştuk.</p>",
                kapak=yer_tutucu("İftar Buluşması"),
            )
            for i in range(3):
                EtkinlikFotografi.objects.create(etkinlik=gecmis, sira=i, aciklama=f"Örnek fotoğraf {i + 1}",
                                                 gorsel=yer_tutucu(f"Örnek fotoğraf {i + 1}", (1200, 800), i))

        self.stdout.write(self.style.SUCCESS("Örnek veri yüklendi."))
