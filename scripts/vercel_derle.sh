#!/usr/bin/env bash
# Vercel derleme adımı (vercel.json → buildCommand).
# Veritabanı kurulumu Vercel'in sunucularından yapılır; böylece yerel ağın 5432/6543 portlarını
# engellemesi sorun olmaz. Ortam değişkenleri Vercel proje ayarlarından gelir.
set -euo pipefail
KOK="$(cd "$(dirname "$0")/.." && pwd)"

if [ -n "${DATABASE_URL:-}" ]; then
  echo "== Python paketleri kuruluyor"
  python3 -m venv /tmp/eskilder-venv
  /tmp/eskilder-venv/bin/pip install --quiet --disable-pip-version-check -r "$KOK/requirements.txt"
  cd "$KOK/backend"
  echo "== Veritabanı tabloları"
  /tmp/eskilder-venv/bin/python manage.py migrate --noinput
  if [ -n "${SUPABASE_S3_ACCESS_KEY:-}" ]; then
    echo "== Örnek içerik (yalnızca veritabanı boşsa)"
    /tmp/eskilder-venv/bin/python manage.py ornek_veri_yukle --sadece-bossa
  fi
  echo "== İlk yönetici hesabı"
  /tmp/eskilder-venv/bin/python manage.py yonetici_olustur
else
  echo "DATABASE_URL tanımlı değil; veritabanı adımları atlandı."
fi

echo "== Site derleniyor"
cd "$KOK/frontend"
npm run build
