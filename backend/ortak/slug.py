from django.utils.text import slugify

_TR = str.maketrans({
    "ı": "i", "İ": "i", "ğ": "g", "Ğ": "g", "ş": "s", "Ş": "s",
    "ç": "c", "Ç": "c", "ö": "o", "Ö": "o", "ü": "u", "Ü": "u",
})


def tr_slugify(metin: str) -> str:
    """Türkçe harfleri ASCII karşılığına çevirip slug üretir (Django slugify 'ı'yı düşürür)."""
    return slugify((metin or "").translate(_TR).replace("_", " ")) or "icerik"


def benzersiz_slug(model, metin: str, haric_pk=None, alan: str = "slug", max_uzunluk: int = 200) -> str:
    taban = tr_slugify(metin)[: max_uzunluk - 6].strip("-") or "icerik"
    aday, sayac = taban, 2
    sorgu = model._default_manager.all()
    if haric_pk is not None:
        sorgu = sorgu.exclude(pk=haric_pk)
    while sorgu.filter(**{alan: aday}).exists():
        aday = f"{taban}-{sayac}"
        sayac += 1
    return aday
