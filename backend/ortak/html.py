import nh3

IZINLI_ETIKETLER = {"p", "br", "strong", "b", "em", "i", "u", "a", "ul", "ol", "li", "h2", "h3", "blockquote"}


def temiz_html(html) -> str:
    """Yönetim panelinden gelen zengin metni beyaz listeye göre temizler. Görsel etiketleri silinir."""
    if not html:
        return ""
    return nh3.clean(
        html,
        tags=IZINLI_ETIKETLER,
        attributes={"a": {"href"}},
        url_schemes={"http", "https", "mailto", "tel"},
        link_rel="noopener noreferrer",
    )
