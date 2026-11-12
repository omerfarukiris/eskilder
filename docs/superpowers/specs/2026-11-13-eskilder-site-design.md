# Eskilder Web Sitesi Yenileme — Tasarım Belgesi

Tarih: 2026-11-13
Durum: Taslak (onay bekliyor)

## 1. Amaç ve neden

Eskilder (Aksaray Eskil kökenli bir dernek), Eskil'den çıkmış üniversite öğrencilerine
karşılıksız burs veriyor. Derneğin geliri Eskilli iş insanlarının bağışlarından geliyor:
memleketlinin memleketliye desteği.

Mevcut site (eskilder.org.tr) statik ve bakımsız:
- son içerik Ocak 2025'e ait;
- `/i/` altında ve kök dizinde birbiriyle çelişen iki sayfa seti var;
- Hakkında sayfası boş, dernek adı sayfadan sayfaya değişiyor;
- iletişim formu ve e-bülten kutusu çalışıyor görünmüyor;
- sosyal medya linkleri boş.

İçerik eklemek zor olduğu için site güncellenmiyor.

Yeni sitenin işi **güven vermek ve iletişimi kolaylaştırmak**:
1. Mevcut destekçilere "desteğiniz doğru yere gidiyor" demek ve onlara görünür bir teşekkür etmek.
2. Derneği ilk kez duyan Eskilli birinin (potansiyel destekçi, öğrenci, veli) derneği ciddiye alması ve kolayca iletişime geçebilmesi.
3. Dernek yöneticilerinin kod bilmeden duyuru, etkinlik/buluşma, destekçi ve rakamları güncel tutabilmesi.

**Başarı ölçütü:** Teknik bilgisi olmayan bir yönetici, yardım almadan 5 dakikada fotoğraflı bir duyuru yayınlayabilir. Siteden gelen iletişim mesajları derneğin e-postasına gerçekten düşer.

### İlk teslim: deneme sürümü

İlk hedef, dernek sorumlularına gösterilecek **çalışan bir deneme sürümüdür.**

- **Barındırma:** Her şey ücretsiz planlarda çalışır (Vercel Hobby, Supabase Free). Hesaplar geliştiricinin kendi hesaplarıdır.
- **Adres:** Site `*.vercel.app` adresinde yayınlanır. eskilder.org.tr alan adına ve DNS'e dokunulmaz.
- **İçerik:** Mevcut sitedeki gerçek içerik kullanılır. Eksik içerikler için gerçekçi yer tutucular konur: logo, rakamlar, destekçiler, fotoğraflar. Yer tutucular panelden kolayca değiştirilebilir.
- **E-posta bildirimi:** İletişim mesajları her durumda panele kaydedilir. E-posta bildirimi yalnızca SMTP bilgileri ortam değişkenlerinde tanımlıysa gönderilir. Deneme sürümünde tanımlı olmayabilir.
- **Yedekleme:** Bu sürümde yok. Uyku önlemi var, çünkü sunum sırasında site kapalı olmamalı.
- **Bakım:** Deneme süresince bakımı geliştirici yapar.

Dernek onay verirse canlıya geçiş ayrı bir adım olarak yapılır:
- hesapların derneğe devri;
- ücretli plan kararı (Vercel Hobby, ticari olmayan kişisel kullanım içindir; derneğin resmî sitesi için Pro gerekebilir);
- alan adı ve eski adres yönlendirmeleri;
- haftalık yedekleme;
- hata uyarıları ve yönetici kılavuzu.

## 2. Hedefler

- Modern, estetik ve mobil uyumlu bir **tanıtım sitesi**. Sitenin tonu sıcak, memleket duygusu taşıyan ve güven veren bir ton olacak.
- **Açılış ekranı:** Eskilder logosuyla kısa bir giriş animasyonu ve ardından logolu, büyük görselli bir karşılama bölümü.
- **Destekçilerimiz:** Bağışçı iş insanları ve firmalar için bir teşekkür duvarı. Yalnızca izin verenler yayınlanır.
- **Destek Ol:** IBAN bilgisi ve "bir öğrencinin bursunu üstlen" çağrısı.
- **Çalışan iletişim:** Konu seçmeli form, telefon, WhatsApp butonu ve harita.
- **Duyurular** ile **Etkinlikler & Buluşmalar.** Etkinliklerin altında fotoğraf galerisi bulunur.
- **Hakkımızda:** Derneğin hikâyesi, amacı ve yönetim kurulu.
- **Burs sayfası:** Kimler başvurabilir, gerekli belgeler, ödeme koşulları ve indirilebilir başvuru formları.
- **Yönetim paneli:** Django Admin, Unfold temasıyla ve Türkçe. Yukarıdaki tüm içerikler buradan yönetilir.

## 3. Hedef dışı (bu sürümde yok)

Bunlar bilerek dışarıda bırakıldı. İkinci sürüme aday olanlar:

- **Çevrim içi burs başvurusu (ikinci sürüm):** Kimlik, banka ve gelir verisi toplanacağı için KVKK, güvenli dosya saklama ve değerlendirme akışı gerektirir. Bu sürümde başvuru, şu anki gibi indirilen form ile sürer.
- **Etkinliklere "Katılacağım" kaydı (ikinci sürüm).**
- **E-bülten ve toplu e-posta gönderimi (ikinci sürüm).** Mevcut sitedeki "E-posta Ekle" kutusu kaldırılır.
- **Şeffaflık raporu ve bursiyer hikâyeleri (ikinci sürüm).**
- **Siteden kartla bağış veya sanal POS:** Bu sürümde yok. Derneklerin internet üzerinden bağış toplaması 2860 sayılı Yardım Toplama Kanunu kapsamında izne tabi olabilir. Bağış yalnızca IBAN ile alınır.
- **Ziyaretçi veya üye girişi, çoklu dil, blog yorumları:** Hiçbir sürümde planlanmıyor.

## 4. Hedef karşıtları (çalışsa bile başarısızlık sayılır)

- Yöneticinin bir duyuru eklemek için geliştiriciye ihtiyaç duyması.
- Açılış animasyonunun ziyaretçiyi bekletmesi veya her sayfa geçişinde tekrar etmesi.
- İzni olmayan bir destekçinin adının sitede görünmesi.
- Siteden gönderilen mesajların hiçbir yere ulaşmaması (mevcut sitedeki sorun).
- WhatsApp'ta paylaşılan duyuru linkinin başlıksız ve görselsiz önizleme vermesi. Duyurular büyük ölçüde WhatsApp gruplarında yayılıyor.
- Sitenin Supabase ücretsiz planı uykuya geçtiği için bir gün açılmaması.

## 5. Kısıtlar

- **Teknoloji (kullanıcının seçimi):** Python/Django, Supabase, Vercel, ön yüzde React ile HTML/CSS/JavaScript.
- **Barındırma:** Vercel'in sunucusuz yapısı. Kalıcı dosya sistemi yok, ilk istek soğuk başlangıçla gelebilir.
- **Yöneticiler teknik değil:** Panel Türkçe, sade ve yönlendirici olmalı.
- **Kişisel veri:** İletişim formu ad, e-posta ve telefon topladığı için KVKK aydınlatma metni gerekir.
- **Alan adı:** eskilder.org.tr korunur. Eski `.html` adresleri yeni sayfalara yönlendirilir.
- **Supabase ücretsiz plan:** Proje 7 gün hareketsiz kalırsa duraklatılıyor. Bunu önlemek için bir önlem şart (bkz. 7.6).

## 6. Yaklaşımlar

Teknoloji yığını kullanıcı tarafından belirlendi. Değerlendirilen asıl soru, yönetim panelinin nasıl yapılacağıydı:

| Yaklaşım | Artısı | Eksisi |
|---|---|---|
| **A. Django Admin + Unfold teması (SEÇİLDİ)** | Hazır giriş, yetki, form ve dosya yükleme. Türkçe. Hızlı ve güvenilir. Modern görünüm. | Görünüm sitenin kendisi kadar özel değil |
| B. Sıfırdan React yönetim paneli | Sitenin tasarımıyla birebir uyumlu, sınırsız özelleştirme | Panel tarafında yaklaşık 3 kat iş. Giriş, yetki ve yükleme baştan yazılır, hata riski yüksek |

**Seçim: A.** Kullanıcı bu yolu seçti. Gerekçesi: Yöneticiler için en önemli şeyler kolaylık ve güvenilirlik. Emek, ziyaretçinin göreceği tarafa harcanmalı.

Ön yüz için Next.js gibi sunucu tarafında sayfa üreten bir çatı da düşünüldü. Kullanıcı React, HTML, CSS ve JavaScript belirttiği için Vite + React tek sayfa uygulaması (SPA) seçildi. SPA'nın paylaşım önizlemesi ve SEO zayıflığı 7.4'teki yöntemle kapatılıyor.

## 7. Tasarım

### 7.1 Mimari

Tek Vercel projesi, tek alan adı:

```
eskilder.org.tr
├── /                    → React SPA (Vite build, statik)
├── /api/...             → Django (Vercel Python runtime) — Django REST Framework, salt-okunur içerik + iletişim formu POST
├── /yonetim/...         → Django Admin (Unfold)
├── /duyurular/<slug>    → Django: index.html'i sayfaya özel <title>/OG meta etiketleriyle döner (bkz. 7.4)
├── /etkinlikler/<slug>  → aynı
└── eski .html adresleri → 301 yönlendirme (vercel.json)
```

- **Veritabanı:** Supabase Postgres. Bağlantı, Supabase connection pooler (transaction mode) üzerinden yapılır. Doğrudan bağlantı kullanılamaz, çünkü IPv6 üzerinden çalışıyor ve Vercel IPv6 desteklemiyor.
  - Django ayarları: `CONN_MAX_AGE=0` ve `DISABLE_SERVER_SIDE_CURSORS=True`.
  - psycopg 3 için ayrıca `OPTIONS={"prepare_threshold": None}` gerekir, çünkü transaction mode prepared statement'ları desteklemiyor.
- **Dosyalar (görseller, PDF/DOCX formlar):** Supabase Storage'da herkese açık bir bucket. Django tarafında `django-storages` ile S3 uyumlu uç nokta kullanılır.
  - Dosya URL'leri S3 uç noktasından değil, Supabase'in herkese açık nesne yolundan üretilir: `AWS_S3_CUSTOM_DOMAIN` ile `/storage/v1/object/public/<bucket>/`.
  - S3 anahtarları tam yetkili olduğu için yalnızca sunucu tarafında kalır.
- **Statik dosyalar:**
  - React derlemesi Vercel CDN'den sunulur.
  - Admin statik dosyaları derleme sırasında `collectstatic` ile toplanır ve WhiteNoise ile sunulur.
- **Derleme sırası:** Önce Vite derlemesi çalışır. Python fonksiyonu, hash'li asset adlarını içeren `dist/index.html` dosyasını paketine dahil eder (vercel.json `includeFiles`). `rewrites` sırası şöyledir: `/api`, `/yonetim`, `/static`, duyuru/etkinlik detay yolları, sonra SPA yedeği.
- **Vercel istek boyutu sınırı (4,5 MB):**
  - Yönetim panelindeki görsel alanlarına küçük bir JS eklenir. Bu kod görseli göndermeden önce tarayıcıda küçültür (en uzun kenar 1920 px, JPEG/WebP, yaklaşık 1 MB altı).
  - Etkinlik galerisinde çoklu fotoğraf yükleme, fotoğrafları tek tek ayrı isteklerle gönderen bir yükleyiciyle yapılır.
  - Belge (PDF/DOCX) sınırı 4 MB'dir. Aşılırsa anlaşılır bir Türkçe hata gösterilir.
  - Yöneticiler telefondan çektikleri fotoğrafı olduğu gibi yükleyebilir.
- **E-posta:** İletişim formu mesajı veritabanına kaydedilir, ardından derneğin e-posta adresine bildirim gönderilir (Django `send_mail`, SMTP ayarları ortam değişkenlerinden). Gönderim başarısız olsa bile mesaj panelde kalır.
- **Gizli bilgiler** (DB URL, Storage anahtarları, SMTP, `SECRET_KEY`) yalnızca Vercel ortam değişkenlerinde tutulur.

### 7.2 Veri modeli (Django modelleri)

- **SiteAyarlari (tekil kayıt):**
  - Kimlik: resmî dernek adı, kısa ad, slogan, logo, açılış (hero) görseli ve hero metni.
  - İletişim: telefon, WhatsApp numarası, e-posta, adres, harita konumu (Google Maps embed linki).
  - Bağış: IBAN, hesap sahibi, banka adı, Destek Ol metni.
  - Sosyal medya linkleri.
  - Sayfa metinleri: Hakkımızda metni, Burs sayfası metni.
  - KVKK aydınlatma metni.
- **EtkiRakami:** etiket (ör. "öğrenciye burs"), değer (ör. "340+"), sıra.
- **Duyuru:** başlık, slug (otomatik), özet, içerik (zengin metin), kapak görseli, yayın tarihi, yayında mı, öne çıkan mı.
- **Etkinlik:**
  - Alanlar: tür (Buluşma / Etkinlik / Burs Töreni / Diğer), başlık, slug, başlangıç tarih-saati, yer, açıklama (zengin metin), kapak görseli, yayında mı.
  - Galeri: **EtkinlikFotografi** (görsel, açıklama, sıra) inline olarak eklenir.
- **Destekci:**
  - Kim olduğu: ad veya firma adı, tür (Kişi / Firma), logo veya fotoğraf (isteğe bağlı), kısa not (ör. "2025'te 3 öğrencinin bursunu üstlendi"), sıra.
  - İzin: **yayın izni var mı (zorunlu onay kutusu; işaretli değilse sitede görünmez)**.
- **YonetimKuruluUyesi:** ad soyad, görev, fotoğraf (isteğe bağlı), sıra.
- **Dokuman:** başlık (ör. "Burs Başvuru Formu 2026"), dosya (PDF veya DOCX), sıra, yayında mı. Burs sayfasında listelenir.
- **IletisimMesaji:**
  - Formdan gelenler: ad soyad, e-posta, telefon (isteğe bağlı), konu (Destekçi olmak istiyorum / Burs hakkında / Diğer), mesaj, KVKK onayı.
  - Otomatik ve yönetim alanları: tarih, durum (Yeni / Okundu / Yanıtlandı).

Zengin metin, Unfold'un WYSIWYG düzenleyicisiyle girilir. Çıktı, sunucuda izin verilen etiketlere göre temizlenir (nh3 veya bleach).

**Metin içine görsel eklenmez.** Görseller kapak görseli ve galeri olarak eklenir. Duyurulara da isteğe bağlı bir galeri (**DuyuruFotografi**) eklenir.

Her kapak görseli için ayrıca paylaşım görseli üretilir: 1200×630, yaklaşık 300 KB altı.

**Saklama süreleri:**
- İletişim mesajları 2 yıl saklanır, sonra otomatik silinir.
- Hız sınırı için tutulan IP kayıtları 24 saat sonra silinir.
- Silme işini günlük cron yapar.

### 7.3 Ziyaretçi sayfaları (React)

| Yol | İçerik |
|---|---|
| `/` | Açılış animasyonu → logolu hero ("Eskil'in çocukları için") + etki rakamları + son 3 duyuru + yaklaşan etkinlik/buluşma + destekçi şeridi + "Destek Ol" ve "İletişime Geç" çağrıları |
| `/hakkimizda` | Dernek hikâyesi/amacı + yönetim kurulu |
| `/burs` | Burs koşulları, belgeler, ödeme bilgisi, indirilebilir formlar |
| `/duyurular`, `/duyurular/:slug` | Liste (sayfalı) ve detay |
| `/etkinlikler`, `/etkinlikler/:slug` | Yaklaşan / geçmiş ayrımı, detayda galeri (lightbox) |
| `/destekcilerimiz` | Teşekkür duvarı (firmalar logolu, kişiler isimle) |
| `/destek-ol` | IBAN (kopyala butonu), "bir öğrencinin bursunu üstlen" çağrısı, iletişim butonu |
| `/iletisim` | Form + telefon + WhatsApp butonu + e-posta + adres + harita |
| `/kvkk` | Aydınlatma metni |
| `*` | 404 sayfası |

**Açılış animasyonu:**
- Logo ortada belirir ve en fazla 1,2 saniye içinde hero bölümüne geçer.
- Ziyaretçi tıklayarak geçebilir.
- Oturum başına bir kez gösterilir (`sessionStorage`).
- `prefers-reduced-motion` açıksa gösterilmez.
- İçerik arkada yüklenir, ziyaretçiyi bekletmez.

**Görsel dil:**
- Renk paleti logodan türetilir.
- Sıcak, sade, bol boşluklu bir tasarım.
- Gerçek fotoğraflar kullanılır: Eskil ve buluşmalar.
- Mobil öncelikli. WCAG AA kontrastı hedeflenir.

**İletişim formu:**
- Gönderim öncesi alanlar doğrulanır.
- KVKK onay kutusu zorunludur.
- Spam koruması: gizli tuzak alan (honeypot) ve IP başına basit bir sınır (ör. saatte 5 mesaj, veritabanında tutulur).
- Gönderimden sonra açık bir başarı veya hata mesajı gösterilir.

### 7.4 Paylaşım önizlemesi ve SEO

Django, duyuru ve etkinlik detay adresleri için SPA'nın `index.html` dosyasını döner. Dönerken içine sayfaya özel `<title>`, `description`, `og:title`, `og:description` ve `og:image` etiketlerini ekler. `og:image`, mutlak bir https adresiyle küçük paylaşım görselini gösterir. Böylece WhatsApp ve Facebook önizlemeleri doğru görünür, React de sayfayı normal şekilde açar.

Diğer sayfalar varsayılan meta etiketlerini kullanır. `sitemap.xml` ve `robots.txt` Django tarafından üretilir.

### 7.5 Yönetim paneli (Django Admin + Unfold)

- Adres `/yonetim/`. Panel Türkçe, logo ve renkler Unfold temasına işlenir.
- **Kenar menüsü:**
  - Ana Sayfa (özet)
  - Duyurular
  - Etkinlikler & Buluşmalar
  - Destekçiler
  - Gelen Mesajlar (yeni mesaj sayısıyla)
  - Etki Rakamları
  - Yönetim Kurulu
  - Belgeler
  - Site Ayarları
  - Kullanıcılar (yalnızca süper yönetici)
- **Özet ekranı:** okunmamış mesaj sayısı, son duyurular ve yaklaşan etkinlikler.
- **Roller:**
  - **Süper yönetici:** teknik kişi, her şeye erişir.
  - **Editör** grubu: içerik modellerini ve mesajları yönetir. Kullanıcılara ve sistem ayarlarına dokunamaz.
- **Kolaylıklar:**
  - Slug otomatik üretilir.
  - Görsel önizlemesi gösterilir.
  - Kayıt eklerken "yayında mı" varsayılan olarak açık gelir. Destekçilerde yayın izni varsayılan olarak kapalı gelir.
  - Sürükle-bırak sıralama (Unfold sortable) kullanılır.
  - Alanların altında kısa Türkçe yardım metinleri bulunur.
  - Mesaj listesinde durum filtresi vardır.
- **Görseller:** Yüklenen görseller büyükse otomatik küçültülür (ör. en uzun kenar 1920 px).

### 7.6 İşletim

- **Uyku önlemi:** Vercel Cron, günde bir kez `/api/saglik` adresini çağırır. Bu uç nokta veritabanına basit bir sorgu atar ve Supabase ücretsiz projesinin duraklatılmasını önler.
  - Uç nokta `CRON_SECRET` ile korunur.
  - Aynı cron, saklama süresi dolan kayıtları da siler.
  - Supabase bu yöntemi resmî bir garanti olarak belgelemiyor. Kesin çözüm Pro plan.
- **IP tespiti:** Hız sınırı için ziyaretçi IP'si `x-forwarded-for` veya `x-real-ip` başlığından okunur. `REMOTE_ADDR` gerçek ziyaretçinin adresi değil.
- **Eski adres yönlendirmeleri** (vercel.json, 301):
  - `anasayfa.html` → `/`
  - `hakkinda.html` → `/hakkimizda`
  - `duyurular.html` → `/duyurular`
  - `iletisim.html` → `/iletisim`
  - `/i/*.html` sayfaları da karşılıklarına yönlendirilir.
- **İçerik taşıma:** Mevcut iki burs duyurusu (2023-2024 ve 2024-2025) ile burs koşulları, başlangıç verisi olarak yeni sisteme aktarılır.
- **Yedekleme:** Supabase ücretsiz planında kullanılabilir otomatik yedek yok. Storage dosyaları hiçbir planda yedeklenmiyor. Bu nedenle haftalık bir yedekleme işi kurulur (ör. GitHub Actions):
  - veritabanının `pg_dump` dökümü alınır;
  - Storage bucket'ı eşitlenir;
  - ikisi şifreli bir arşiv olarak dernek hesabındaki bir depolamaya kaydedilir.
  - Ayrıntı, 8. bölümdeki plan ve hesap kararına bağlıdır.

## 8. Kullanıcının karar verdikleri

- **Amaç:** Eskil kökenli öğrencilere burs; güven vermek, destekçileri görünür kılmak, iletişimi kolaylaştırmak.
- **Açılış:** Logo ilk ekranda öne çıkacak.
- **Buluşmalar:** Etkinlikler bölümünün parçası olacak.
- **Teknoloji:** Django, Supabase, Vercel, React ile HTML/CSS/JS.
- **Panel:** Django Admin + Unfold.
- **Online burs başvurusu:** İkinci sürüme bırakıldı. Bu benim önerimdi; kullanıcı itiraz etmeden "başlayabilirsin" dedi.
- **İlk teslim:** Dernek sorumlularına gösterilecek deneme sürümü, tamamen ücretsiz planlarda.

## 9. Benim kararlarım (kullanıcı düzeltebilir)

- **Ön yüz:** Vite + React + React Router. TypeScript yerine JavaScript. Stil için düz CSS (CSS Modules), CSS çatısı yok.
- **Kurulum:** Tek Vercel projesi, tek alan adı.
- **Yönetim paneli adresi:** `/yonetim/`.
- **Açılış animasyonu:** Oturumda bir kez ve 1,2 saniye üst sınırla.
- **İletişim formu:** Honeypot ve basit hız sınırı. Captcha ancak spam gelirse eklenir.
- **Paylaşım:** WhatsApp ve Facebook önizlemesi için Django'nun meta etiketi enjekte etmesi.
- **Uyku önlemi:** Supabase'in uykuya geçmemesi için günlük cron.
- **İçerik taşıma:** Eski iki duyurunun taşınması.
- **Büyük dosyalar:** Görseller yüklenmeden önce tarayıcıda küçültülür ve galeri fotoğrafları tek tek yüklenir (Vercel'in 4,5 MB sınırı yüzünden).
- **Metin içi görsel yok:** Görseller kapak ve galeri olarak eklenir.
- **Saklama süreleri:** Mesajlar 2 yıl, IP kayıtları 24 saat.
- **KVKK aydınlatma metni:** Ben şablon taslağını hazırlarım, dernek kontrol eder ve onaylar.

## 10. Kurucuya bırakılanlar

- Proje dizin yapısı, paket sürümleri, test araçları.
- Bileşen tasarımının ayrıntıları ve animasyon kütüphanesi (CSS veya hafif bir kütüphane).
- Sayfalama boyutu, görsel küçültme kütüphanesi (Pillow).
- API uç noktalarının tam şekli.

## 11. Kullanıcıdan gelecek içerik ve erişimler

Deneme sürümü için hiçbiri zorunlu değil. Eksik olanların yerine yer tutucu kullanılır. Canlıya geçmeden önce hepsi gerekli:

- Yüksek çözünürlüklü logo (SVG veya PNG).
- Hero için fotoğraflar: Eskil, öğrenciler, buluşmalar.
- Resmî dernek adı. Sitede iki farklı ad geçiyor.
- Etki rakamları: kuruluş yılı, toplam bursiyer sayısı, varsa diğerleri.
- Yönetim kurulu listesi ve Hakkımızda metni.
- İzin alınmış destekçi listesi.
- Telefon ve WhatsApp numarası, IBAN bilgisi, sosyal medya hesapları.
- Mesaj bildirimleri için e-posta gönderim hesabı (ör. eskilder68@gmail.com için uygulama şifresi).
- eskilder.org.tr alan adının DNS yönetimine erişim.
- Supabase ve Vercel hesapları.
