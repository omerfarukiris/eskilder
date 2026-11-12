# Eskilder — dernek sitesi (deneme sürümü)

Eskil kökenli üniversite öğrencilerine burs veren Eskilder derneğinin tanıtım sitesi ve yönetim paneli.

- **Ön yüz:** Vite + React (`frontend/`)
- **Sunucu ve yönetim paneli:** Django + DRF + Unfold (`backend/`), Vercel Python fonksiyonu olarak çalışır (`api/index.py`)
- **Veritabanı ve dosyalar:** Supabase Postgres ve Supabase Storage
- Tasarım belgesi: `docs/superpowers/specs/2026-11-13-eskilder-site-design.md`

## Yerelde çalıştırma

```bash
python3.12 -m venv .venv && .venv/bin/pip install -r backend/requirements-dev.txt
cd backend && export DEBUG=1
../.venv/bin/python manage.py migrate
../.venv/bin/python manage.py ornek_veri_yukle
../.venv/bin/python manage.py createsuperuser
../.venv/bin/python manage.py runserver 8000
```

Ayrı bir terminalde:

```bash
cd frontend && npm install && npm run dev
```

- Site: http://localhost:5173
- Yönetim paneli: http://localhost:8000/yonetim/

`DATABASE_URL` tanımlı değilse SQLite, `SUPABASE_S3_ENDPOINT` tanımlı değilse yerel dosya sistemi kullanılır.

## Testler

```bash
cd backend && ../.venv/bin/pytest -q
```

```bash
cd frontend && npx vitest run
```

## Admin statik dosyaları

Unfold'un CSS ve JS dosyaları `frontend/public/static/` altında repoya eklenmiştir ve Vercel CDN'inden sunulur. Python bağımlılıkları güncellendiğinde aşağıdaki betiği çalıştırıp çıktıyı commit edin:

```bash
./scripts/collectstatic.sh
```

## Yayın (Vercel + Supabase, ücretsiz planlar)

### Supabase

1. Supabase'te bir proje açın (bölge: `eu-central-1`).
2. **Storage** bölümünde `medya` adında **herkese açık (public)** bir bucket oluşturun.
3. **Storage → S3 Connection** bölümünden bir erişim anahtarı üretin. Bu ekran size endpoint ve bölge bilgisini de verir.
4. **Connect → Transaction pooler** bölümünden bağlantı adresini kopyalayın (port **6543**). Adresteki şifreyi kendi veritabanı şifrenizle değiştirin.

### Vercel ortam değişkenleri

| Değişken | Örnek |
|---|---|
| `SECRET_KEY` | uzun rastgele bir metin |
| `DATABASE_URL` | `postgresql://postgres.<ref>:<şifre>@aws-0-eu-central-1.pooler.supabase.com:6543/postgres` |
| `ALLOWED_HOSTS` | `.vercel.app` |
| `SITE_URL` | `https://<proje>.vercel.app` |
| `CRON_SECRET` | uzun rastgele bir metin |
| `SUPABASE_S3_ENDPOINT` | `https://<ref>.supabase.co/storage/v1/s3` |
| `SUPABASE_S3_REGION` | `eu-central-1` |
| `SUPABASE_S3_ACCESS_KEY` / `SUPABASE_S3_SECRET_KEY` | Storage → S3 erişim anahtarı |
| `SUPABASE_PUBLIC_URL` | `https://<ref>.supabase.co` |
| `SUPABASE_BUCKET` | `medya` |
| `EMAIL_HOST`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD` (isteğe bağlı) | Gmail için `smtp.gmail.com` ve bir uygulama şifresi |

### İlk kurulum

Yukarıdaki değişkenler yerel ortamınızda da tanımlıyken (`DEBUG` olmadan) şu komutları çalıştırın:

```bash
cd backend
../.venv/bin/python manage.py migrate
../.venv/bin/python manage.py createsuperuser
../.venv/bin/python manage.py ornek_veri_yukle
```

Vercel, GitHub deposundan otomatik derler. Ayarlar `vercel.json` dosyasındadır. Günlük cron (`/api/saglik/`), Supabase'in uykuya geçmesini önler ve süresi dolan kayıtları siler.

## Yönetim paneli kullanımı

- **Editör rolü:** Yeni bir yönetici için *Kullanıcılar* bölümünden kullanıcı oluşturun. "Yönetici durumu" kutusunu işaretleyin ve kullanıcıyı **Editör** grubuna ekleyin. Editörler içerikleri ve gelen mesajları yönetebilir, kullanıcı ayarlarına erişemez.
- **Destekçi izni:** Destekçiler, ancak "Sitede yayınlanmasına izin verdi" kutusu işaretlenirse sitede görünür.
