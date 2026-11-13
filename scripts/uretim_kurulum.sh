#!/usr/bin/env bash
# Yayındaki (Supabase) veritabanını kurar. Ayarları ../.env dosyasından okur.
#   ./scripts/uretim_kurulum.sh tablolar   -> yalnız tabloları kurar (S3 anahtarı gerekmez)
#   ./scripts/uretim_kurulum.sh            -> tablolar + örnek içerik (görseller Supabase Storage'a yüklenir)
set -euo pipefail
cd "$(dirname "$0")/.."
if grep -q "^DATABASE_URL=BURAYA_" .env; then echo "Önce .env dosyasındaki DATABASE_URL değerini doldurun."; exit 1; fi
set -a; source .env; set +a
cd backend
../.venv/bin/python manage.py migrate
if [ "${1:-}" = "tablolar" ]; then echo "Tablolar kuruldu."; exit 0; fi
if grep -q "^SUPABASE_S3_.*=BURAYA_" ../.env; then echo "Örnek içerik için önce .env'deki S3 anahtarlarını doldurun."; exit 1; fi
../.venv/bin/python manage.py ornek_veri_yukle
echo "Tamam. Şimdi yönetici hesabını oluşturun:  ./scripts/uretim_yonetici.sh"
