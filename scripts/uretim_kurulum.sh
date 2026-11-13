#!/usr/bin/env bash
# Yayındaki (Supabase) veritabanına tabloları kurar ve örnek içeriği yükler. Ayarları ../.env dosyasından okur.
set -euo pipefail
cd "$(dirname "$0")/.."
if grep -q "BURAYA_" .env; then echo "Önce .env dosyasındaki BURAYA_ ile başlayan değerleri doldurun."; exit 1; fi
set -a; source .env; set +a
cd backend
../.venv/bin/python manage.py migrate
../.venv/bin/python manage.py ornek_veri_yukle
echo "Tamam. Şimdi yönetici hesabını oluşturun:  cd backend && set -a && source ../.env && set +a && ../.venv/bin/python manage.py createsuperuser"
