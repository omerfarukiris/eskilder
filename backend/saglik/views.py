import hmac

from django.conf import settings
from django.db import connection
from django.http import JsonResponse
from django.views.decorators.http import require_GET

from iletisim.servis import eski_kayitlari_temizle


def _yetkili(request) -> bool:
    gizli = settings.CRON_SECRET
    if not gizli:
        return False
    gelen = request.headers.get("Authorization", "")
    return hmac.compare_digest(gelen.encode(), f"Bearer {gizli}".encode())


@require_GET
def saglik(request):
    """Vercel Cron günde bir çağırır: veritabanını uyanık tutar, eski kayıtları temizler."""
    if not _yetkili(request):
        return JsonResponse({"hata": "yetkisiz"}, status=401)
    with connection.cursor() as imlec:
        imlec.execute("SELECT 1")
    silinen_mesaj, silinen_ip = eski_kayitlari_temizle()
    return JsonResponse({"durum": "ok", "silinen_mesaj": silinen_mesaj, "silinen_ip": silinen_ip})
