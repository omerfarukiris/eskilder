# Eskilder Deneme Sürümü — Uygulama Planı

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Hedef:** Eskilder derneğinin yeni tanıtım sitesini ve Django Admin (Unfold) yönetim panelini kurmak. Sonuç, dernek sorumlularına gösterilecek ve `*.vercel.app` adresinde, ücretsiz planlarda çalışan bir deneme sürümü olacak.

**Mimari:**
- Tek Vercel projesi:
  - `frontend/` (Vite + React SPA) statik olarak CDN'den sunulur.
  - `api/index.py`, Django'yu Vercel Python fonksiyonu olarak çalıştırır. Django şunlara cevap verir: `/api/*`, `/yonetim/*`, duyuru/etkinlik detay sayfalarının meta etiketli HTML'i, `sitemap.xml` ve `robots.txt`.
- Veri: Supabase Postgres (pooler üzerinden).
- Dosyalar: Supabase Storage (S3 uyumlu, `django-storages`).

**Teknoloji:**
- Python 3.12, Django 5.2 LTS, Django REST Framework, django-unfold, psycopg 3, django-storages[s3], Pillow, nh3, dj-database-url, pytest-django.
- Node 20, Vite, React 18, React Router 6, Vitest, Testing Library.

**Spec:** `docs/superpowers/specs/2026-11-13-eskilder-site-design.md`. Planın her görevi bu belgeye dayanır, uygulayıcı ikisini birlikte okur.

## Genel Kısıtlar

- Kullanıcıya görünen tüm metinler Türkçe. Panel dili `tr`, saat dilimi `Europe/Istanbul`.
- Ön yüz JavaScript ile yazılır (TypeScript yok). Stil için düz CSS / CSS Modules kullanılır, CSS çatısı yok.
- Ücretsiz planlar: Vercel Hobby ve Supabase Free. Site `*.vercel.app` adresinde yayınlanır, eskilder.org.tr DNS'ine dokunulmaz.
- Vercel istek gövdesi sınırı 4,5 MB. Tek istekte gönderilen hiçbir yükleme bunu aşamaz.
  - Görseller tarayıcıda en uzun kenar 1920 px'e küçültülür (yaklaşık 1 MB altı).
  - Belgeler en fazla 4 MB olabilir.
- Veritabanı ayarları: `CONN_MAX_AGE=0`, `DISABLE_SERVER_SIDE_CURSORS=True`, `OPTIONS={"prepare_threshold": None}`.
- Storage URL'leri `https://<proje>.supabase.co/storage/v1/object/public/<bucket>/` üzerinden üretilir. S3 anahtarları yalnızca sunucuda tutulur.
- Gizli bilgiler yalnızca ortam değişkenlerinde tutulur: `SECRET_KEY`, `DATABASE_URL`, `SUPABASE_S3_*`, `SUPABASE_PUBLIC_URL`, `SUPABASE_BUCKET`, `CRON_SECRET`, `EMAIL_*`, `SITE_URL`, `ALLOWED_HOSTS`.
- Açılış animasyonu:
  - en fazla 1,2 saniye sürer;
  - oturum başına bir kez gösterilir (`sessionStorage`);
  - tıklayınca geçilir;
  - `prefers-reduced-motion` açıksa gösterilmez.
- Destekçi yalnızca `yayin_izni=True` ise sitede görünür. `yayin_izni` varsayılan olarak `False` gelir.
- İletişim formu:
  - honeypot alanı içerir;
  - IP başına saatte en fazla 5 mesaj kabul eder;
  - IP, `x-forwarded-for` başlığının ilk değerinden alınır, yoksa `x-real-ip`'ten;
  - KVKK onayı zorunludur.
- Saklama süreleri: iletişim mesajları 2 yıl (730 gün), IP kayıtları 24 saat.
- Paylaşım görseli 1200×630 px ve 300 KB altı olur. `og:image` mutlak https adresi kullanır.
- Zengin metin, `nh3` ile beyaz liste üzerinden temizlenir. Metin içine görsel eklenmez.

## İnceleme Odağı

Spec'in ima ettiği ama gözden kaçması en olası beş durum (her biri, ilgili görevde bir testle sabitlenir):

1. **Türkçe karakterli başlıklar** ("Burs Başvuruları Işık", "İftar Buluşması"). Slug okunur ASCII olmalı (`burs-basvurulari-isik`, `iftar-bulusmasi`). Django `slugify`, `ı`/`İ` harflerini düşürür. Aynı başlık ikinci kez girilirse slug `-2` ile ayrışmalı (Görev 2).
2. **Telefon fotoğrafı.** EXIF'e göre yan duran fotoğraf düz kaydedilmeli. Desteklenmeyen format (ör. HEIC) yüklenirse çökme yerine Türkçe hata verilmeli (Görev 3).
3. **İzinsiz destekçi.** `yayin_izni=False` olan destekçi hiçbir uçtan dönmemeli: destekçi listesi, ana sayfa şeridi (Görev 5).
4. **Yayında olmayan içerik.** Yayında olmayan ya da yayın tarihi gelecekte olan bir duyurunun detay API'si de, meta etiketli HTML sayfası da 404 dönmeli (Görev 5 ve 8).
5. **E-posta gönderimi başarısız olsa bile mesaj kaybolmamalı.** SMTP tanımsızken ya da hata verirken form 201 dönmeli ve mesaj panelde görünmeli (Görev 6).

---

## Dosya Yapısı

```
eskilder/
├── vercel.json                  # build’ler, rewrite sırası, cron
├── requirements.txt             # Vercel Python fonksiyonu için (backend/requirements.txt'e -r)
├── api/index.py                 # Vercel giriş noktası: `app = config.wsgi.application`
├── scripts/collectstatic.sh     # admin statiklerini frontend/public/static/ altına toplar
├── backend/
│   ├── manage.py
│   ├── requirements.txt
│   ├── pytest.ini
│   ├── config/{settings.py,urls.py,wsgi.py}
│   ├── ortak/                   # yardımcılar: slug, html temizleme, görsel, ip
│   │   ├── slug.py  html.py  gorsel.py  ip.py
│   ├── icerik/                  # içerik modelleri, admin, API, OG sayfaları, seed komutu
│   │   ├── models.py admin.py api.py serializers.py og.py sitemap.py
│   │   ├── management/commands/ornek_veri_yukle.py
│   │   └── static/icerik/admin/gorsel_kucult.js, galeri_yukle.js
│   ├── iletisim/                # mesaj modeli, POST uç noktası, hız sınırı, temizlik
│   │   ├── models.py admin.py api.py servis.py
│   ├── saglik/                  # cron uç noktası
│   │   └── views.py
│   └── tests/                   # pytest testleri, uygulama başına bir dosya
└── frontend/
    ├── index.html  vite.config.js  package.json
    ├── public/static/           # collectstatic çıktısı (commit edilir)
    └── src/
        ├── main.jsx  App.jsx  api.js  stil/{tema.css,genel.css}
        ├── bilesenler/{Ust.jsx,Alt.jsx,Acilis.jsx,Lightbox.jsx,Kart.jsx,Sayfalama.jsx,...}
        └── sayfalar/{Anasayfa,Hakkimizda,Burs,Duyurular,DuyuruDetay,Etkinlikler,EtkinlikDetay,Destekciler,DestekOl,Iletisim,Kvkk,Bulunamadi}.jsx
```

**Kararlar (spec'ten sapma veya spec'in bıraktığı yerler):**
- **Admin statik dosyaları:** WhiteNoise kullanılmıyor. `scripts/collectstatic.sh` ile `frontend/public/static/` altına toplanıp commit edilir ve Vercel CDN'den sunulur. Böylece fonksiyon paketi küçük kalır ve derleme sırası sorunu oluşmaz.
- **Meta etiketli HTML:** Django, SPA'nın `index.html` dosyasını kendi paketinde aramaz. Dosyayı çalışma anında `SITE_URL + "/index.html"` adresinden çeker ve 5 dakika bellekte tutar. Bu yöntem hash'li asset adlarından bağımsızdır.
- **Testler:** Yerelde ve testte `DATABASE_URL` yoksa SQLite kullanılır. Storage ayarları yoksa yerel `FileSystemStorage` kullanılır.

---

### Task 1: Depo iskeleti, Django ayarları, sağlık uç noktası

**Dosyalar:**
- Oluştur:
  - `.gitignore`, `requirements.txt`
  - `backend/manage.py`, `backend/requirements.txt`, `backend/pytest.ini`
  - `backend/config/settings.py`, `backend/config/urls.py`, `backend/config/wsgi.py`
  - `backend/saglik/views.py`, `api/index.py`
- Test: `backend/tests/test_saglik.py`

**Arayüzler:**
- Üretir:
  - `config.wsgi.application`
  - `GET /api/saglik/` uç noktası: `Authorization: Bearer <CRON_SECRET>` başlığıyla çağrılır, `{"durum": "ok", "silinen_mesaj": int, "silinen_ip": int}` döner.
  - Görev 6, bu uç noktaya `iletisim.servis.eski_kayitlari_temizle()` çağrısını ekler. Görev 6 yapılana kadar sayılar 0 döner.

- [ ] **Adım 1:** `git init`. Ardından `.gitignore` oluştur: `__pycache__`, `.venv`, `node_modules`, `frontend/dist`, `backend/media`, `.env*`, `db.sqlite3`.

- [ ] **Adım 2:** `backend/requirements.txt` dosyasını sabit sürümlerle yaz: `Django==5.2.*`, `djangorestframework`, `django-unfold`, `psycopg[binary]`, `dj-database-url`, `django-storages[s3]`, `boto3`, `Pillow`, `nh3`, `pytest`, `pytest-django`. Kök dizindeki `requirements.txt` yalnızca `-r backend/requirements.txt` içerir.

- [ ] **Adım 3: Başarısız testleri yaz**

```python
def test_saglik_gizli_anahtar_olmadan_401(client, settings):
    settings.CRON_SECRET = "s3cr3t"
    assert client.get("/api/saglik/").status_code == 401

def test_saglik_yanlis_anahtar_401(client, settings):
    settings.CRON_SECRET = "s3cr3t"
    r = client.get("/api/saglik/", HTTP_AUTHORIZATION="Bearer yanlis")
    assert r.status_code == 401

def test_saglik_dogru_anahtar_200(client, settings):
    settings.CRON_SECRET = "s3cr3t"
    r = client.get("/api/saglik/", HTTP_AUTHORIZATION="Bearer s3cr3t")
    assert r.status_code == 200 and r.json()["durum"] == "ok"
```

- [ ] **Adım 4:** `cd backend && pytest tests/test_saglik.py -v` çalıştır. Beklenen: FAIL.

- [ ] **Adım 5: `settings.py`'yi uygula**
  - Tüm ayarlar ortam değişkenlerinden okunur.
  - `DATABASE_URL` yoksa `sqlite:///db.sqlite3` kullanılır. Varsa Genel Kısıtlar'daki üç veritabanı ayarı eklenir.
  - `LANGUAGE_CODE="tr"`, `TIME_ZONE="Europe/Istanbul"`, `STATIC_URL="/static/"`, `STATIC_ROOT=BASE_DIR.parent/"frontend/public/static"`.
  - Admin yolu `yonetim/`.
  - `CRON_SECRET` boşsa uç nokta her zaman 401 döner.
  - Anahtar karşılaştırması `hmac.compare_digest` ile yapılır.
  - `api/index.py`, `sys.path`'e `backend/` ekler ve `app = application` tanımlar.

- [ ] **Adım 6:** Testleri tekrar çalıştır. Beklenen: PASS. Ayrıca `python manage.py check` hatasız geçmeli.

- [ ] **Adım 7: Commit** — `chore: django iskeleti ve sağlık uç noktası`

---

### Task 2: Ortak yardımcılar (slug, HTML temizleme) ve içerik modelleri

**Dosyalar:**
- Oluştur: `backend/ortak/slug.py`, `backend/ortak/html.py`, `backend/icerik/models.py` (+ migration)
- Test: `backend/tests/test_slug_html.py`, `backend/tests/test_icerik_modelleri.py`

**Arayüzler:**
- Üretir:
  - `tr_slugify(metin: str) -> str`
  - `benzersiz_slug(model, metin: str, haric_pk=None) -> str`
  - `temiz_html(html: str) -> str`. İzinli etiketler: `p, br, strong, b, em, i, u, a(href), ul, ol, li, h2, h3, blockquote`. `a` etiketine `rel="noopener"` eklenir, `img` silinir.
- Modeller: alan adları birebir aşağıdaki gibidir. Sonraki görevler bu adlara güvenir.

| Model | Alanlar |
|---|---|
| `SiteAyarlari` (tekil, `SiteAyarlari.yukle()` → pk=1 get_or_create) | `resmi_ad, kisa_ad, slogan, logo(Image), hero_gorsel(Image), hero_metin, telefon, whatsapp, eposta, adres, harita_embed_url, iban, hesap_sahibi, banka, destek_ol_metni(Text), hakkimizda_metni(Text, HTML), burs_metni(Text, HTML), kvkk_metni(Text, HTML), facebook, instagram, x, youtube` (hepsi boş geçilebilir, URL alanları URLField) |
| `EtkiRakami` | `etiket, deger(Char, "340+"), sira(int)` |
| `Duyuru` | `baslik, slug(unique, editable=False), ozet(Char 300), icerik(Text HTML), kapak(Image, null), paylasim_gorseli(Image, null, editable=False), yayin_tarihi(DateTime, default now), yayinda(bool, True), one_cikan(bool, False)`; ordering `-yayin_tarihi` |
| `DuyuruFotografi` | `duyuru(FK, related_name="fotograflar"), gorsel, aciklama, sira` |
| `Etkinlik` | `tur(choices: bulusma/etkinlik/burs_toreni/diger), baslik, slug, baslangic(DateTime), yer, aciklama(Text HTML), kapak, paylasim_gorseli, yayinda(True)`; ordering `-baslangic` |
| `EtkinlikFotografi` | `etkinlik(FK, related_name="fotograflar"), gorsel, aciklama, sira` |
| `Destekci` | `ad, tur(choices: kisi/firma), logo(Image, null), not_metni(Char 200), sira, yayin_izni(bool, **False**)` |
| `YonetimKuruluUyesi` | `ad_soyad, gorev, fotograf(null), sira` |
| `Dokuman` | `baslik, dosya(File, uzantı pdf/doc/docx, ≤4 MB validator), sira, yayinda(True)` |

Tüm modellerde `verbose_name` ve `help_text` Türkçe yazılır (panel bunları gösterir). `Duyuru.save()` ve `Etkinlik.save()`:
- slug boşsa `benzersiz_slug` ile üretir;
- `icerik`/`aciklama` alanını `temiz_html` ile temizler.

Paylaşım görseli üretimi Görev 3'te eklenir.

- [ ] **Adım 1: Başarısız testleri yaz**

```python
@pytest.mark.parametrize("girdi,beklenen", [
    ("Burs Başvuruları Işık", "burs-basvurulari-isik"),
    ("İftar Buluşması", "iftar-bulusmasi"),
    ("Öğrenci Çay Sohbeti  !!", "ogrenci-cay-sohbeti"),
])
def test_tr_slugify(girdi, beklenen): assert tr_slugify(girdi) == beklenen

def test_ayni_baslik_ikinci_kez_ayri_slug(db):
    a = Duyuru.objects.create(baslik="Burs Duyurusu")
    b = Duyuru.objects.create(baslik="Burs Duyurusu")
    assert (a.slug, b.slug) == ("burs-duyurusu", "burs-duyurusu-2")

def test_slug_baslik_degisince_sabit_kalir(db):
    d = Duyuru.objects.create(baslik="Eski"); d.baslik = "Yeni"; d.save()
    assert d.slug == "eski"

def test_temiz_html_script_ve_img_siler():
    assert temiz_html('<p>a<script>x</script><img src=x onerror=y></p>') == "<p>a</p>"

def test_destekci_varsayilan_izinsiz(db):
    assert Destekci.objects.create(ad="X", tur="firma").yayin_izni is False

def test_site_ayarlari_tekil(db):
    assert SiteAyarlari.yukle().pk == SiteAyarlari.yukle().pk == 1

def test_dokuman_4mb_ustu_reddedilir(db): ...  # 4*1024*1024+1 baytlık SimpleUploadedFile ile full_clean → ValidationError
```

- [ ] **Adım 2:** Testleri çalıştır. Beklenen: FAIL (import hatası).

- [ ] **Adım 3:** Yardımcıları ve modelleri uygula.
  - `tr_slugify`, önce `str.translate` ile Türkçe harfleri çevirir: `ı→i, İ→i, ğ→g, Ğ→g, ş→s, Ş→s, ç→c, Ç→c, ö→o, Ö→o, ü→u, Ü→u`. Sonra Django `slugify` çalışır.
  - Slug boş kalırsa `"icerik"` kullanılır.
  - Ardından `makemigrations icerik` çalıştırılır.

- [ ] **Adım 4:** Testleri çalıştır. Beklenen: PASS.

- [ ] **Adım 5: Commit** — `feat: içerik modelleri ve Türkçe slug`

---

### Task 3: Görsel işleme ve depolama

**Dosyalar:**
- Oluştur: `backend/ortak/gorsel.py`
- Değiştir: `backend/icerik/models.py` (kapak/görsel kaydında işleme), `backend/config/settings.py` (STORAGES)
- Test: `backend/tests/test_gorsel.py`, `backend/tests/test_depolama.py`

**Arayüzler:**
- Üretir:
  - `kucult(dosya, en_uzun=1920) -> ContentFile`. Dosyayı EXIF yönüne göre döndürür, JPEG kalite 85 ile kaydeder ve EXIF'i siler.
  - `paylasim_gorseli_uret(dosya) -> ContentFile`. 1200×630 boyutunda merkezden kırpar. JPEG kalitesini 85'ten başlayıp 5'er düşürür, ta ki dosya 300 KB altına inene kadar (en düşük 50).
  - `GorselHatasi(ValidationError)`, mesajı: "Bu görsel biçimi desteklenmiyor. Lütfen JPG veya PNG yükleyin."

`Duyuru` ve `Etkinlik`: `kapak` değiştiğinde (önceki ad ile karşılaştırılır) kapağı `kucult` ile küçültür ve `paylasim_gorseli` dosyasını yeniden üretir. Galeri ve destekçi logo görselleri yalnızca `kucult`'tan geçer. Model `clean()` metodunda Pillow dosyayı açamazsa `GorselHatasi` fırlatılır.

**Depolama:**
- `SUPABASE_S3_ENDPOINT` tanımlıysa `default` storage `storages.backends.s3.S3Storage` olur. Ayarlar:
  - `bucket_name=SUPABASE_BUCKET`
  - `endpoint_url=SUPABASE_S3_ENDPOINT`
  - `region_name=SUPABASE_S3_REGION`
  - `custom_domain=f"{host}/storage/v1/object/public/{bucket}"` (host, `SUPABASE_PUBLIC_URL`'den şemasız alınır)
  - `querystring_auth=False`, `file_overwrite=False`
- Tanımlı değilse yerel `FileSystemStorage` kullanılır (`MEDIA_ROOT=backend/media`).

- [ ] **Adım 1: Başarısız testleri yaz**

```python
def test_kucult_en_uzun_kenar_1920(): # 4000x3000 JPEG → (1920, 1440)
def test_kucult_exif_yonu_uygulanir(): # 100x50 + EXIF Orientation=6 → çıktı (50, 100), EXIF yok
def test_paylasim_gorseli_boyut_ve_agirlik(): # gürültülü 3000x2000 → (1200,630) ve len < 300*1024
def test_bozuk_dosya_gorsel_hatasi(): # b"HEIC değil" baytları → GorselHatasi
def test_kapak_degisince_paylasim_gorseli_olusur(db): # Duyuru(kapak=...) save → paylasim_gorseli dolu
def test_s3_url_supabase_public_yolu(settings): # ortam ayarlanınca default_storage.url("a.jpg") ==
    # "https://abc.supabase.co/storage/v1/object/public/medya/a.jpg"
```

- [ ] **Adım 2:** Testleri çalıştır. Beklenen: FAIL.

- [ ] **Adım 3:** `gorsel.py` dosyasını uygula (`ImageOps.exif_transpose` kullanılır). Ardından model kayıt kancalarını ve storage ayarını ekle.

- [ ] **Adım 4:** Testleri çalıştır. Beklenen: PASS.

- [ ] **Adım 5: Commit** — `feat: görsel küçültme, paylaşım görseli ve Supabase depolama`

---

### Task 4: Örnek veri komutu

**Dosyalar:**
- Oluştur: `backend/icerik/management/commands/ornek_veri_yukle.py`, `backend/icerik/ornek_veri/` (yer tutucu görseller)
- Test: `backend/tests/test_ornek_veri.py`

**Arayüzler:**
- Üretir: `python manage.py ornek_veri_yukle` komutu. İki kez çalıştırıldığında kayıtları çoğaltmaz (`get_or_create`, anahtar `baslik`/`ad`).

**İçerik (mevcut siteden alınan gerçek bilgiler):**
- **Dernek adı:** `resmi_ad="Eskil Kültür Eğitim ve Dayanışma Derneği"`. Bu ad, kullanıcı netleştirene kadar yer tutucudur, panelden değiştirilir. `kisa_ad="Eskilder"`.
- **İletişim:**
  - `eposta="eskilder68@gmail.com"`
  - `adres="Çelebi Mah. Şehit Battal Yıldız Sk. Derinpark Sitesi No: 1/CF Karatay/Konya"`
- **Duyurular:**
  - "2024-2025 Eğitim Öğretim Dönemi Burs Başvuruları Başladı" (yayın tarihi 2024-12-23)
  - "2023-2024 Eğitim Öğretim Yılı İçin Burs Başvurularını Başlatıyoruz" (yayın tarihi 2023-11-08)
- **Burs metni:**
  - Başvuru koşulu: Aksaray'ın Eskil ilçesine kayıtlı üniversite öğrencileri.
  - Burs karşılıksızdır.
  - Ödemeler her ayın 25–30'u arasında öğrencinin hesabına yapılır.
  - İmzalı, fotoğraflı form kargo veya PTT ile gönderilir.

**Yer tutucular** (adların başına "Örnek" yazılır ki panelde fark edilsin):
- 4 etki rakamı
- 6 destekçi: 4'ü `yayin_izni=True`, 2'si `False`
- 3 yönetim kurulu üyesi
- 2 etkinlik: 1 yaklaşan buluşma, 1 geçmiş buluşma (3 galeri fotoğrafıyla)
- KVKK metni taslağı. Başına "Taslak — dernek tarafından kontrol edilmelidir" notu eklenir.

- [ ] **Adım 1: Başarısız testi yaz**

```python
def test_ornek_veri_iki_kez_calisinca_cogalmaz(db):
    call_command("ornek_veri_yukle"); call_command("ornek_veri_yukle")
    assert Duyuru.objects.count() == 2 and Destekci.objects.count() == 6
    assert Destekci.objects.filter(yayin_izni=True).count() == 4
```

- [ ] **Adım 2:** Testi çalıştır. Beklenen: FAIL.
- [ ] **Adım 3:** Komutu uygula.
- [ ] **Adım 4:** Testi çalıştır. Beklenen: PASS.
- [ ] **Adım 5: Commit** — `feat: örnek veri komutu`

---

### Task 5: Salt-okunur içerik API'si

**Dosyalar:**
- Oluştur: `backend/icerik/serializers.py`, `backend/icerik/api.py`
- Değiştir: `backend/config/urls.py`
- Test: `backend/tests/test_icerik_api.py`

**Arayüzler** (Görev 10–13'teki ön yüz bu yanıt şekillerine bağlıdır):
- Görsel alanlar mutlak URL ya da `null` döner. Tarihler ISO 8601 biçimindedir.
- `GET /api/ayarlar/` döner:
  - SiteAyarlari'nin tüm alanları
  - `rakamlar: [{etiket, deger}]`
  - `kurul: [{ad_soyad, gorev, fotograf}]`
  - `dokumanlar: [{baslik, dosya}]`
- `GET /api/duyurular/?sayfa=N` döner: `{count, next, previous, results: [{baslik, slug, ozet, kapak, yayin_tarihi, one_cikan}]}`. Sayfa boyutu 9. Yalnızca `yayinda=True` ve `yayin_tarihi<=now` olan kayıtlar listelenir.
- `GET /api/duyurular/<slug>/` döner: listedeki alanlar + `icerik` + `fotograflar: [{gorsel, aciklama}]`. Kayıt yayında değilse ya da yayın tarihi gelecekteyse 404.
- `GET /api/etkinlikler/?zaman=yaklasan|gecmis&sayfa=N`:
  - `yaklasan` için `baslangic>=now`, artan sırada.
  - `gecmis` için `baslangic<now`, azalan sırada.
  - Her kayıt: `{tur, tur_adi, baslik, slug, baslangic, yer, kapak}`.
- `GET /api/etkinlikler/<slug>/` döner: listedeki alanlar + `aciklama` + `fotograflar`.
- `GET /api/destekciler/` döner: `[{ad, tur, logo, not_metni}]`. Yalnızca `yayin_izni=True` olanlar, `sira` düzenine göre. Sayfalama yok.
- Tüm uçlar herkese açık ve salt okunurdur. `Cache-Control: public, max-age=60` başlığı eklenir.

- [ ] **Adım 1: Başarısız testleri yaz**
  - `test_izinsiz_destekci_listede_yok`
  - `test_yayinda_olmayan_duyuru_listede_ve_detayda_yok` (detay 404 döner)
  - `test_gelecek_tarihli_duyuru_detay_404`
  - `test_duyuru_sayfalama_9`: 10 kayıtla `count==10`, `len(results)==9`
  - `test_etkinlik_yaklasan_gecmis_ayrimi`
  - `test_ayarlar_rakam_ve_kurul_sirali`
  - `test_post_405`: içerik uçlarına POST gönderilince 405 döner

- [ ] **Adım 2:** Testleri çalıştır. Beklenen: FAIL.
- [ ] **Adım 3:** DRF `ReadOnlyModelViewSet` ve `lookup_field="slug"` ile uygula. Sayfalama parametresi `sayfa`.
- [ ] **Adım 4:** Testleri çalıştır. Beklenen: PASS.
- [ ] **Adım 5: Commit** — `feat: içerik API'si`

---

### Task 6: İletişim formu uç noktası, hız sınırı, temizlik

**Dosyalar:**
- Oluştur: `backend/iletisim/models.py`, `backend/iletisim/api.py`, `backend/iletisim/servis.py`, `backend/ortak/ip.py`
- Değiştir: `backend/saglik/views.py`
- Test: `backend/tests/test_iletisim.py`

**Arayüzler:**
- Modeller:
  - `IletisimMesaji`: `ad_soyad, eposta, telefon(blank), konu(choices: destekci/burs/diger), mesaj, kvkk_onay, olusturma(auto_now_add), durum(choices: yeni/okundu/yanitlandi, default yeni)`
  - `IpKaydi`: `ip, zaman(auto_now_add)`
- `istemci_ip(request) -> str`: önce `HTTP_X_FORWARDED_FOR`'un ilk değerini (kırpılmış) dener, sonra `HTTP_X_REAL_IP`, en son `REMOTE_ADDR`.
- `POST /api/iletisim/` JSON gövdesi: `{ad_soyad, eposta, telefon?, konu, mesaj, kvkk_onay, web_sitesi}`. `web_sitesi` alanı honeypot'tur.
  - Başarılı: `201 {"tamam": true}`.
  - Doğrulama hatası: `400 {alan: [Türkçe mesaj]}`.
  - Sınır aşıldı: `429 {"hata": "Çok fazla mesaj gönderildi. Lütfen bir saat sonra tekrar deneyin."}`.
  - `web_sitesi` doluysa: `201` döner ama mesaj kaydedilmez (bot farkı anlamasın).
- `bildirim_gonder(mesaj: IletisimMesaji) -> bool`:
  - `EMAIL_HOST` boşsa `False` döner.
  - Gönderimi `send_mail` ile `SiteAyarlari.eposta` adresine yapar.
  - İstisnaları yakalar, loglar ve `False` döner.
- `eski_kayitlari_temizle(simdi=None) -> tuple[int, int]`: 730 günden eski mesajları ve 24 saatten eski IP kayıtlarını siler. Silinen sayıları döner. Sağlık uç noktası bu fonksiyonu çağırır.

- [ ] **Adım 1: Başarısız testleri yaz**
  - `test_gecerli_mesaj_201_ve_kaydedilir`
  - `test_kvkk_onaysiz_400`
  - `test_gecersiz_eposta_400`
  - `test_bos_mesaj_400`
  - `test_honeypot_dolu_201_ama_kayit_yok`
  - `test_ayni_ip_altinci_mesaj_429`: 5 mesaj 201 döner, 6. mesaj 429 döner
  - `test_farkli_x_forwarded_for_ayri_sayilir`: `HTTP_X_FORWARDED_FOR="1.1.1.1, 10.0.0.1"` ile `"2.2.2.2"` ayrı sayılır
  - `test_smtp_hata_verse_de_201_ve_kayit_var`: `send_mail` mock'u istisna fırlatır
  - `test_temizlik_731_gunluk_mesaji_siler_729u_birakir`
  - `test_temizlik_25_saatlik_ip_siler`
  - `test_saglik_temizligi_cagirir`

- [ ] **Adım 2:** Testleri çalıştır. Beklenen: FAIL.
- [ ] **Adım 3:** Uygula. Hız sınırı, son 1 saatteki `IpKaydi` sayısına bakar. Sayı 5 veya daha fazlaysa istek 429 alır. Değilse kayıt eklenir.
- [ ] **Adım 4:** Testleri çalıştır. Beklenen: PASS.
- [ ] **Adım 5: Commit** — `feat: iletişim formu uç noktası`

---

### Task 7: Yönetim paneli (Unfold)

**Dosyalar:**
- Oluştur: `backend/icerik/admin.py`, `backend/iletisim/admin.py`, `backend/icerik/static/icerik/admin/gorsel_kucult.js`, `backend/icerik/static/icerik/admin/galeri_yukle.js`, `backend/icerik/migrations/00xx_editor_grubu.py`, `backend/icerik/views_yonetim.py`
- Değiştir: `backend/config/settings.py` (`UNFOLD` ayarı)
- Test: `backend/tests/test_yonetim.py`

**Arayüzler:**
- `UNFOLD` ayarı:
  - `SITE_TITLE="Eskilder Yönetim"`
  - Kenar menüsü spec 7.5'teki sırayla. "Gelen Mesajlar" öğesinin rozetinde `durum=yeni` sayısı gösterilir. "Kullanıcılar" öğesi yalnızca süper yöneticiye görünür.
  - `DASHBOARD_CALLBACK="icerik.views_yonetim.ozet"`. Bu callback, okunmamış mesaj sayısını, son 5 duyuruyu ve yaklaşan 3 etkinliği verir.
- Editör grubu (data migration ile oluşturulur):
  - Verilen izinler: içerik modelleri ve `IletisimMesaji` için ekleme, değiştirme, silme, görüntüleme.
  - Verilmeyen: `auth` modelleri.
- `POST /yonetim/galeri-yukle/<model>/<pk>/`:
  - Yalnızca staff kullanıcılar çağırabilir ve CSRF korumalıdır.
  - `<model>` değeri `duyuru` veya `etkinlik` olabilir.
  - Tek dosya alır. Dosya `kucult`'tan geçer.
  - Başarılıysa `{"id", "gorsel"}` döner. Hata durumunda Türkçe mesajla 400 döner.
- `gorsel_kucult.js`:
  - Paneldeki tüm `input[type=file][accept^=image]` alanlarına eklenir.
  - Seçilen dosyayı canvas ile en uzun kenarı 1920 px olacak şekilde JPEG'e (kalite 0.85) çevirir ve input'taki dosyayla değiştirir (`DataTransfer`).
- `galeri_yukle.js`:
  - Duyuru ve etkinlik değişiklik sayfasında "Fotoğrafları toplu ekle" alanı gösterir.
  - Çoklu seçilen dosyaları önce küçültür, sonra tek tek yükler. Her dosya için ilerleme gösterir.
  - Bitince sayfayı yeniler.

**Admin sınıfları:**
- Bütün içerik admin'leri Unfold `ModelAdmin` sınıfından türer.
- Sıralanabilir modeller `ordering_field="sira"` kullanır: EtkiRakami, Destekci, YonetimKuruluUyesi, Dokuman ve fotoğraf inline'ları.
- Zengin metin alanlarında Unfold WYSIWYG widget'ı kullanılır.
- Listelerde küçük görsel önizlemesi gösterilir.
- `Destekci` listesinde `yayin_izni` sütunu ve filtresi bulunur.
- `IletisimMesaji`:
  - Alanları salt okunurdur, yalnızca `durum` değiştirilebilir.
  - Mesaj açıldığında `yeni` ise otomatik `okundu` olur.
  - Durum ve konu filtreleri vardır. Ekleme yetkisi yoktur.
- `SiteAyarlari` için ekleme ve silme kapalıdır. Liste sayfası doğrudan pk=1 değişiklik sayfasına yönlendirir.

- [ ] **Adım 1: Başarısız testleri yaz**
  - `test_editor_kullanicilara_erisemez`: `/yonetim/auth/user/` adresi 403 döner
  - `test_editor_duyuru_ekleyebilir`: admin add formuna POST gönderilir, sonuç 302 ve kayıt oluşur
  - `test_mesaj_acilinca_okundu_olur`
  - `test_site_ayarlari_listesi_tekil_kayda_yonlenir`
  - `test_galeri_yukle_staff_olmayan_403`
  - `test_galeri_yukle_gorsel_ekler`
  - `test_galeri_yukle_bozuk_dosya_400_turkce_mesaj`
  - `test_ozet_okunmamis_sayisi`

- [ ] **Adım 2:** Testleri çalıştır. Beklenen: FAIL.
- [ ] **Adım 3:** Admin sınıflarını, migration'ı, callback'i, galeri görünümünü ve iki JS dosyasını uygula.
- [ ] **Adım 4:** Testleri çalıştır. Beklenen: PASS.
- [ ] **Adım 5: Elle doğrulama**
  1. `python manage.py runserver` ile sunucuyu başlat ve `/yonetim/` adresinde süper kullanıcıyla giriş yap.
  2. 4000 px'lik bir telefon fotoğrafını kapak olarak yükle. Ağ sekmesinde istek gövdesinin 1,5 MB altında olduğunu gör.
  3. 5 fotoğrafı toplu yükle.
  4. Arayüzün Türkçe olduğunu kontrol et.
- [ ] **Adım 6: Commit** — `feat: Unfold yönetim paneli`

---

### Task 8: Paylaşım meta sayfaları, sitemap, robots

**Dosyalar:**
- Oluştur: `backend/icerik/og.py`, `backend/icerik/sitemap.py`
- Değiştir: `backend/config/urls.py`
- Test: `backend/tests/test_og.py`

**Arayüzler:**
- `spa_index_html() -> str`: `settings.SITE_URL + "/index.html"` adresini 3 saniye zaman aşımıyla çeker ve sonucu 300 saniye modül içi önbellekte tutar. Çekim başarısız olursa önbellekteki son değer kullanılır. O da yoksa, `<div id="root"></div>` ve `/` adresine yönlendiren bir script içeren minimal bir HTML döner.
- `meta_ekle(html: str, baslik: str, aciklama: str, gorsel_url: str | None, url: str) -> str`:
  - Mevcut `<title>` etiketini değiştirir.
  - `</head>` etiketinden önce şunları ekler: `description`, `og:title`, `og:description`, `og:image`, `og:url`, `og:type=article`, `twitter:card=summary_large_image`.
  - Değerler HTML kaçışlıdır (`html.escape`).
- Görünümler `GET /duyurular/<slug>` ve `GET /etkinlikler/<slug>` (sonda `/` olsa da olmasa da çalışır):
  - Görev 5'teki görünürlük kuralları geçerlidir. Görünmüyorsa SPA HTML'i 404 durum koduyla döner.
  - `og:image` için paylaşım görseli kullanılır. Yoksa SiteAyarlari'ndaki logo kullanılır.
- `GET /sitemap.xml`: statik sayfaları ve yayındaki duyuru ve etkinlikleri listeler. `GET /robots.txt`: `/yonetim/` adresine izin vermez ve sitemap adresini belirtir.

- [ ] **Adım 1: Başarısız testleri yaz** (`spa_index_html` mock'lanır)
  - `test_duyuru_og_etiketleri`: başlık ve açıklama doğru yerleşir, `og:image` `https://` ile başlar
  - `test_baslikta_tirnak_kacislanir`: `Ali "Usta"` başlığı `&quot;` olur
  - `test_yayinda_olmayan_duyuru_og_404`
  - `test_index_cekilemezse_yedek_html_200`
  - `test_sitemap_yayindakileri_icerir_taslagi_icermez`
  - `test_robots_yonetimi_engeller`
- [ ] **Adım 2:** Testleri çalıştır. Beklenen: FAIL.
- [ ] **Adım 3:** Uygula.
- [ ] **Adım 4:** Testleri çalıştır. Beklenen: PASS.
- [ ] **Adım 5: Commit** — `feat: paylaşım önizlemesi, sitemap ve robots`

---

### Task 9: Ön yüz iskeleti, tema, düzen, API istemcisi

**Dosyalar:**
- Oluştur: `frontend/` (Vite React JS şablonu), `src/api.js`, `src/App.jsx`, `src/stil/tema.css`, `src/stil/genel.css`, `src/bilesenler/Ust.jsx`, `src/bilesenler/Alt.jsx`, `src/sayfalar/Bulunamadi.jsx`
- Test: `frontend/src/__tests__/api.test.js`, `frontend/src/__tests__/Ust.test.jsx`

**Arayüzler:**
- `api.js`:
  - `getir(yol: string) -> Promise<any>`. Yol `/api` önekiyle çağrılır. Yanıt `!ok` ise `ApiHatasi(durum)` fırlatılır.
  - `gonder(yol, veri) -> Promise<{durum, govde}>`
  - `useVeri(yol) -> {veri, yukleniyor, hata}` hook'u.
  - `AyarlarSaglayici` context'i, `/api/ayarlar/` verisini bir kez çeker. `useAyarlar()` hook'u bu veriyi verir.
- Rotalar (`App.jsx`): spec 7.3'teki tablo birebir uygulanır, `*` rotası `Bulunamadi` sayfasına gider.
- Geliştirme ortamında `vite.config.js` proxy'si `/api`, `/yonetim`, `/static` isteklerini `http://127.0.0.1:8000` adresine yönlendirir.
- `tema.css` dosyasındaki CSS değişkenleri:
  - Renkler: `--renk-ana`, `--renk-ana-koyu`, `--renk-vurgu`, `--renk-zemin`, `--renk-yuzey`, `--renk-metin`, `--renk-metin-soluk`
  - Diğer: `--yaricap`, `--golge`, `--icerik-genislik: 1120px`
  - Ana renk logodan alınır. Logo gelene kadar sıcak bir koyu yeşil ve toprak tonu vurgu yer tutucu olarak kullanılır.
  - Fontlar Google Fonts'tan gelir: başlıklar için bir serif (Fraunces), metin için Inter.
  - Mobil öncelikli tasarlanır. Kırılım noktaları 640 ve 1024 px.
- `Ust.jsx`: logo, menü öğeleri, mobilde hamburger menü ve "Destek Ol" butonu.
- `Alt.jsx`: iletişim bilgileri, sosyal medya bağlantıları ve KVKK linki. Sosyal medya bağlantılarından yalnızca dolu olanlar gösterilir.

- [ ] **Adım 1: Başarısız testleri yaz**
  - `getir 404'te ApiHatasi(404) fırlatır`
  - `Ust mobilde menü butonuna tıklayınca bağlantılar görünür, bağlantıya tıklayınca kapanır`
  - `Bilinmeyen rota Bulunamadi gösterir`
- [ ] **Adım 2:** `cd frontend && npx vitest run` çalıştır. Beklenen: FAIL.
- [ ] **Adım 3:** Uygula.
- [ ] **Adım 4:** `npx vitest run` ve `npm run build` çalıştır. Beklenen: PASS ve derleme başarılı.
- [ ] **Adım 5: Commit** — `feat: ön yüz iskeleti ve tema`

---

### Task 10: Açılış animasyonu ve ana sayfa

**Dosyalar:**
- Oluştur: `src/bilesenler/Acilis.jsx`, `Acilis.module.css`, `src/sayfalar/Anasayfa.jsx`, `Anasayfa.module.css`, `src/bilesenler/Kart.jsx`
- Test: `src/__tests__/Acilis.test.jsx`, `src/__tests__/Anasayfa.test.jsx`

**Arayüzler:**
- `<Acilis />`:
  - `App` içinde, rotaların üstünde render edilir.
  - Görünür olup olmayacağına `acilisGosterilsinMi(storage, matchMedia) -> bool` karar verir. Bu fonksiyon ayrıca dışa aktarılır.
  - `sessionStorage["acilis_goruldu"]` değeri `"1"` ise ya da `prefers-reduced-motion: reduce` eşleşiyorsa `false` döner.
  - `sessionStorage` erişimi hata verirse (gizli mod) gösterim yine yapılır, ama hata fırlatılmaz.
  - Animasyon en fazla 1200 ms sürer, sonra bileşen kaldırılır. Tıklama veya Esc tuşu animasyonu hemen kapatır.
  - İçerik arkada normal şekilde yüklenir.
- `Anasayfa` bölümleri, sırayla:
  1. Hero: arka planda `hero_gorsel`, üstünde logo, `hero_metin` ve iki buton ("Destek Ol" → `/destek-ol`, "Bize Ulaşın" → `/iletisim`).
  2. Etki rakamları.
  3. Son 3 duyuru kartı.
  4. Yaklaşan etkinlik kartı (yoksa bölüm gizlenir).
  5. Destekçi şeridi (yoksa gizlenir) ve "Tüm destekçilerimiz" bağlantısı.
  6. "Bir öğrencinin bursunu üstlenin" çağrı bandı.

- [ ] **Adım 1: Başarısız testleri yaz**
  - `acilisGosterilsinMi`: ilk ziyarette true; `acilis_goruldu=1` ise false; reduced-motion açıksa false; storage hata verirse true döner ve fırlatmaz
  - `Acilis 1200 ms sonra kaldırılır`: fake timers ile
  - `Acilis tıklayınca hemen kapanır`
  - `Anasayfa yaklaşan etkinlik yoksa o bölümü göstermez`
- [ ] **Adım 2:** Testleri çalıştır. Beklenen: FAIL.
- [ ] **Adım 3:** Uygula.
- [ ] **Adım 4:** Testleri çalıştır. Beklenen: PASS.
- [ ] **Adım 5: Elle doğrulama** — 375 px ve 1280 px genişlikte ekran görüntüsü al. Açılış animasyonu yeni sekmede bir kez oynamalı, sayfa yenilenince tekrar oynamamalı.
- [ ] **Adım 6: Commit** — `feat: açılış animasyonu ve ana sayfa`

---

### Task 11: İçerik sayfaları

**Dosyalar:**
- Oluştur:
  - `src/sayfalar/Hakkimizda.jsx`, `Burs.jsx`, `Duyurular.jsx`, `DuyuruDetay.jsx`, `Etkinlikler.jsx`, `EtkinlikDetay.jsx`, `Destekciler.jsx`, `DestekOl.jsx`, `Kvkk.jsx`
  - `src/bilesenler/Lightbox.jsx`, `Sayfalama.jsx`, `HtmlIcerik.jsx`
  - her biri için `.module.css`
- Test: `src/__tests__/DestekOl.test.jsx`, `Lightbox.test.jsx`, `Detay.test.jsx`

**Arayüzler:**
- `<HtmlIcerik html={...} />`: sunucuda temizlenmiş HTML'i `dangerouslySetInnerHTML` ile basar. Bu yalnızca sunucu içeriği `temiz_html`'den geçirdiği için güvenlidir (Görev 2).
- Detay sayfaları API'den 404 alırsa `Bulunamadi` sayfasını gösterir. Sayfa `document.title` değerini içerik başlığına ayarlar.
- `Etkinlikler` sayfasında "Yaklaşan" ve "Geçmiş" sekmeleri vardır. Varsayılan sekme yaklaşan etkinliklerdir; hiç yaklaşan etkinlik yoksa geçmiş sekmesi açılır.
- `<Lightbox fotograflar index onKapat />`: ok tuşlarıyla gezilir, Esc ile kapanır. Mobilde kaydırma hareketi desteklenir.
- `DestekOl`:
  - IBAN 4'lü gruplar halinde gösterilir.
  - "IBAN'ı Kopyala" butonu `navigator.clipboard.writeText` ile IBAN'ı boşluksuz kopyalar ve 2 saniye boyunca "Kopyalandı" yazar.
  - Pano erişilemezse IBAN metni seçili hale getirilir.
  - IBAN boşsa "IBAN bilgisi yakında eklenecek" yazar.
- `Burs` sayfası `burs_metni` ve `dokumanlar` listesini (indirme bağlantıları) gösterir.
- `Destekciler` sayfasında firmalar logolu kart olarak, kişiler isim listesi olarak gösterilir.

- [ ] **Adım 1: Başarısız testleri yaz**
  - `IBAN kopyalanınca boşluksuz yazılır ve "Kopyalandı" görünür`
  - `IBAN boşsa yakında mesajı`
  - `Lightbox Esc ile kapanır, sağ ok sonraki fotoğraf`
  - `DuyuruDetay API 404 → Bulunamadi`
- [ ] **Adım 2:** Testleri çalıştır. Beklenen: FAIL.
- [ ] **Adım 3:** Uygula.
- [ ] **Adım 4:** Testleri çalıştır. Beklenen: PASS.
- [ ] **Adım 5: Commit** — `feat: içerik sayfaları`

---

### Task 12: İletişim sayfası

**Dosyalar:**
- Oluştur: `src/sayfalar/Iletisim.jsx`, `Iletisim.module.css`
- Test: `src/__tests__/Iletisim.test.jsx`

**Arayüzler:**
- Kullanır: `gonder("/iletisim/", veri)` (Görev 6 sözleşmesi).
- Form alanları: Ad Soyad, E-posta, Telefon (isteğe bağlı), Konu (Destekçi olmak istiyorum / Burs hakkında / Diğer), Mesaj ve KVKK onay kutusu (`/kvkk` bağlantılı).
- `web_sitesi` alanı görsel olarak gizlenir. `aria-hidden`, `tabIndex=-1` ve `autocomplete=off` ile işaretlenir.
- İstemci tarafı doğrulama: zorunlu alanlar, e-posta biçimi ve KVKK onayı. Hatalar Türkçe olarak alanın altında gösterilir.
- Sunucu yanıtları:
  - 201: form kaybolur, "Mesajınız bize ulaştı. En kısa sürede dönüş yapacağız." yazar.
  - 400: alan hataları ilgili alanların altında gösterilir.
  - 429 ve ağ hatası: formun üstünde hata mesajı çıkar. Girilen değerler korunur.
- Gönderim sürerken buton devre dışıdır ve "Gönderiliyor…" yazar.
- Yan panelde şunlar bulunur:
  - Telefon: `tel:` bağlantısı.
  - WhatsApp: `https://wa.me/<yalnızca rakamlar>` bağlantısı.
  - E-posta: `mailto:` bağlantısı.
  - Adres ve harita (`harita_embed_url` doluysa `iframe` ile, `loading="lazy"`).

- [ ] **Adım 1: Başarısız testleri yaz**
  - `KVKK işaretlenmeden gönderilemez`
  - `201 sonrası teşekkür mesajı`
  - `400 alan hatası ilgili alanın altında`
  - `429'da değerler korunur ve hata görünür`
  - `WhatsApp linki numaradaki boşluk/+ işaretlerini temizler`
- [ ] **Adım 2:** Testleri çalıştır. Beklenen: FAIL.
- [ ] **Adım 3:** Uygula.
- [ ] **Adım 4:** Testleri çalıştır. Beklenen: PASS.
- [ ] **Adım 5: Commit** — `feat: iletişim sayfası`

---

### Task 13: Vercel ve Supabase kurulumu, yayın, duman testi

**Dosyalar:**
- Oluştur: `vercel.json`, `scripts/collectstatic.sh`, `README.md` (kurulum, ortam değişkenleri, yönetici kullanıcısı oluşturma)
- Değiştir: `frontend/public/static/` (collectstatic çıktısı)

**Arayüzler:**
- `vercel.json`:
  - `builds`:
    - `api/index.py` → `@vercel/python`
    - `frontend/package.json` → `@vercel/static-build`, `distDir: "dist"`
  - `routes` (sırayla):
    1. `/api/(.*)` → `api/index.py`
    2. `/yonetim(.*)` → `api/index.py`
    3. `/duyurular/[^/]+/?` → `api/index.py`
    4. `/etkinlikler/[^/]+/?` → `api/index.py`
    5. `/sitemap.xml` ve `/robots.txt` → `api/index.py`
    6. `{"handle": "filesystem"}`
    7. `/(.*)` → `/frontend/index.html`
  - `crons`: günde bir kez `/api/saglik/` (`0 6 * * *`).
- `scripts/collectstatic.sh`: `cd backend && python manage.py collectstatic --noinput --clear`. Çıktı `frontend/public/static/` altına yazılır.

- [ ] **Adım 1: Supabase hazırlığı**
  - Supabase'te ücretsiz bir proje aç (bölge: eu-central).
  - `medya` adında herkese açık bir Storage bucket'ı oluştur ve S3 erişim anahtarı üret.
  - Pooler (transaction, 6543) bağlantı adresini al.
  - Yerelde `DATABASE_URL` ile şunları çalıştır: `python manage.py migrate`, `createsuperuser`, `ornek_veri_yukle`. Örnek görseller bu adımda bucket'a yüklenir.
- [ ] **Adım 2:** `scripts/collectstatic.sh` betiğini çalıştır ve `frontend/public/static/unfold/` klasörünün oluştuğunu doğrula.
- [ ] **Adım 3:** Vercel'de projeyi oluştur ve ortam değişkenlerini Genel Kısıtlar'daki listeye göre gir. `SITE_URL` ve `ALLOWED_HOSTS` değerleri `*.vercel.app` adresidir. Sonra yayınla.
- [ ] **Adım 4: Duman testi** (yayındaki adreste)
  1. `/` açılır, açılış animasyonu oynar, duyurular görünür.
  2. `/duyurular/<slug>` sayfasının kaynağında `og:image` vardır.
  3. `/api/saglik/` anahtarsız 401, anahtarla 200 döner.
  4. `/yonetim/` adresinde giriş yapılır, panel stilleri yüklüdür.
  5. Telefondan bir fotoğraf yüklenip duyuru yayınlanır, sitede görünür.
  6. İletişim formundan gönderilen mesaj panelde görünür.
  7. Bilinmeyen bir adres 404 sayfası gösterir.
  8. Mobil (375 px) görünüm kontrol edilir.
- [ ] **Adım 5: Commit** — `chore: Vercel yapılandırması ve kurulum belgesi`

---

## Spec Kapsam Eşlemesi

| Spec | Görev |
|---|---|
| 7.1 Mimari, DB, depolama, 4,5 MB | 1, 3, 7, 13 |
| 7.2 Veri modeli, zengin metin, saklama | 2, 3, 6 |
| 7.3 Sayfalar, açılış, görsel dil, form | 9–12 |
| 7.4 Paylaşım/SEO | 8 |
| 7.5 Panel, roller, kolaylıklar | 7 |
| 7.6 Uyku önlemi, IP, içerik taşıma | 1, 6, 4, 13 |
| Deneme sürümü kapsamı (vercel.app, yer tutucular, SMTP isteğe bağlı) | 4, 6, 13 |

Canlıya geçişe bırakılanlar bu planda yok, bilerek: alan adı, eski URL yönlendirmeleri, yedekleme, hata uyarıları ve kılavuz.
