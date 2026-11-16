#!/usr/bin/env bash
# .env dosyasındaki eksik gizli değerleri sorar ve dosyaya yazar. Yazdıklarınız ekranda görünmez.
set -euo pipefail
cd "$(dirname "$0")/.."

yaz() {  # yaz ANAHTAR DEGER  -> .env'de ANAHTAR= satırını günceller
  ANAHTAR="$1" DEGER="$2" python3 - <<'PY'
import os
anahtar, deger = os.environ["ANAHTAR"], os.environ["DEGER"]
satirlar = open(".env", encoding="utf-8").read().splitlines()
satirlar = [f"{anahtar}={deger}" if s.startswith(anahtar + "=") else s for s in satirlar]
open(".env", "w", encoding="utf-8").write("\n".join(satirlar) + "\n")
PY
}

sor() {  # sor ANAHTAR "açıklama"
  if grep -q "^$1=BURAYA_" .env; then
    echo
    echo "$2"
    read -r -s -p "Yapıştırın ve Enter'a basın (ekranda görünmez): " deger
    echo
    if [ -z "$deger" ]; then echo "  Boş bırakıldı, atlandı."; return; fi
    yaz "$1" "$deger"
    echo "  Kaydedildi (${#deger} karakter)."
  fi
}

echo "Supabase → https://supabase.com/dashboard/project/ihadeyfjtszrvqzsxphs/settings/storage"
echo "S3 Access Keys bölümünde 'New access key' ile bir anahtar oluşturun."
sor SUPABASE_S3_ACCESS_KEY "1/3  Access key ID:"
sor SUPABASE_S3_SECRET_KEY "2/3  Secret access key:"
sor YONETICI_SIFRE "3/3  Yayındaki yönetim paneli için belirlediğiniz şifre (en az 8 karakter):"

echo
if grep -q "=BURAYA_" .env; then echo "Hâlâ eksik değer var:"; grep -o "^[A-Z_]*=BURAYA_" .env | cut -d= -f1; else echo "Tamam, .env tamamen dolu."; fi
