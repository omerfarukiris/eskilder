#!/usr/bin/env bash
# Yayındaki yönetim paneli kullanıcısının şifresini sıfırlamak için SQL hazırlar ve panoya kopyalar.
# Şifre ekranda görünmez; yalnızca Django'nun tek yönlü özeti (hash) üretilir.
# Çıkan SQL'i Supabase → SQL Editor'e yapıştırıp çalıştırın.
set -euo pipefail
cd "$(dirname "$0")/../backend"

read -r -p "Kullanıcı adı [omerfarukiris]: " kullanici
kullanici="${kullanici:-omerfarukiris}"
if ! [[ "$kullanici" =~ ^[A-Za-z0-9_.@+-]+$ ]]; then echo "Geçersiz kullanıcı adı."; exit 1; fi

while true; do
  read -r -s -p "Yeni şifre (en az 8 karakter, ekranda görünmez): " s1; echo
  read -r -s -p "Yeni şifre (tekrar): " s2; echo
  if [ "$s1" != "$s2" ]; then echo "Şifreler aynı değil, tekrar deneyin."; continue; fi
  if [ "${#s1}" -lt 8 ]; then echo "En az 8 karakter olmalı."; continue; fi
  break
done

ozet=$(SIFRE="$s1" DEBUG=1 ../.venv/bin/python -c "
import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
os.environ.pop('DATABASE_URL', None)
django.setup()
from django.contrib.auth.hashers import make_password
print(make_password(os.environ['SIFRE']))
")
unset s1 s2

sql="update auth_user set password = '${ozet}', is_active = true where username = '${kullanici}' returning username;"
printf '%s' "$sql" | pbcopy
echo
echo "Hazır. SQL komutu panoya kopyalandı (şifrenin kendisi değil, özeti)."
echo "Şimdi: Supabase → SQL Editor → yapıştırın (⌘V) → Run."
echo "Sonuçta '${kullanici}' satırı görünürse şifre değişmiştir."
