#!/usr/bin/env bash
# Yayındaki yönetim paneli kullanıcısının adını ve/veya şifresini değiştirmek için SQL hazırlar (.yonetici.sql).
# Şifre ekranda görünmez; yalnızca Django'nun tek yönlü özeti (hash) üretilir.
# Çıkan SQL'i Supabase → SQL Editor'e yapıştırıp çalıştırın.
set -euo pipefail
cd "$(dirname "$0")/../backend"

gecerli() { [[ "$1" =~ ^[A-Za-z0-9_.@+-]{1,150}$ ]]; }

read -r -p "Şu anki kullanıcı adı [omerfarukiris]: " eski
eski="${eski:-omerfarukiris}"
gecerli "$eski" || { echo "Geçersiz kullanıcı adı."; exit 1; }

read -r -p "Yeni kullanıcı adı (değiştirmeyecekseniz boş bırakıp Enter): " yeni
yeni="${yeni:-$eski}"
gecerli "$yeni" || { echo "Kullanıcı adında yalnızca harf, rakam ve _ . @ + - olabilir (Türkçe karakter ve boşluk olmaz)."; exit 1; }

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

sql="update auth_user set username = '${yeni}', password = '${ozet}', is_active = true where username = '${eski}' returning username;"
( umask 077; printf '%s\n' "$sql" > ../.yonetici.sql )
echo
echo "Hazır. Komut proje klasöründeki gizli .yonetici.sql dosyasına yazıldı (şifrenin kendisi değil, özeti)."
echo "Claude'a 'hazır' deyin; Supabase'te o çalıştıracak ve dosyayı silecek."
echo "Kendiniz yapmak isterseniz: dosyanın içeriğini Supabase → SQL Editor'e yapıştırıp Run'a basın."
