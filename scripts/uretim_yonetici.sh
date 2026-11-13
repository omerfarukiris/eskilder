#!/usr/bin/env bash
# Yayındaki (Supabase) veritabanında yönetici hesabı oluşturur. Kullanıcı adı ve şifreyi siz girersiniz.
set -euo pipefail
cd "$(dirname "$0")/.."
set -a; source .env; set +a
cd backend
../.venv/bin/python manage.py createsuperuser
