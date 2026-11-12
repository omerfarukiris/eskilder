def istemci_ip(request) -> str:
    """Vercel proxy arkasında gerçek ziyaretçi IP'si: x-forwarded-for'un ilki, sonra x-real-ip."""
    ileri = request.META.get("HTTP_X_FORWARDED_FOR", "")
    if ileri.strip():
        return ileri.split(",")[0].strip()
    gercek = request.META.get("HTTP_X_REAL_IP", "").strip()
    return gercek or request.META.get("REMOTE_ADDR", "")
