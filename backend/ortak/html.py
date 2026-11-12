import nh3

# Unfold (Trix) düzenleyicisi paragrafları <div> olarak yazar; başlık ve biçim düğmelerinin etiketleri de izinli.
IZINLI_ETIKETLER = {
    "p", "div", "br", "strong", "b", "em", "i", "u", "del", "s", "a", "ul", "ol", "li",
    "h1", "h2", "h3", "h4", "blockquote", "pre", "code",
}


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
