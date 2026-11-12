#!/usr/bin/env bash
# Django admin (Unfold) statik dosyalarını frontend/public/static/ altına toplar.
# Vite bunları derlemede dist/static/ altına kopyalar; Vercel CDN'den sunulur.
# Bağımlılık sürümleri değişince yeniden çalıştırıp commit edin.
set -euo pipefail
cd "$(dirname "$0")/../backend"
DEBUG=1 ../.venv/bin/python manage.py collectstatic --noinput --clear -v0
echo "Statik dosyalar: frontend/public/static/ ($(du -sh ../frontend/public/static | cut -f1))"
