import pytest

from ortak.html import temiz_html
from ortak.slug import tr_slugify


@pytest.mark.parametrize(
    "girdi,beklenen",
    [
        ("Burs Başvuruları Işık", "burs-basvurulari-isik"),
        ("İftar Buluşması", "iftar-bulusmasi"),
        ("Öğrenci Çay Sohbeti  !!", "ogrenci-cay-sohbeti"),
        ("ĞÜŞİÖÇ ğüşıöç", "gusioc-gusioc"),
    ],
)
def test_tr_slugify(girdi, beklenen):
    assert tr_slugify(girdi) == beklenen


def test_tr_slugify_bos_kalirsa_icerik():
    assert tr_slugify("!!!") == "icerik"


def test_temiz_html_script_ve_img_siler():
    assert temiz_html('<p>a<script>x</script><img src=x onerror=y></p>') == "<p>a</p>"


def test_temiz_html_izinli_etiketleri_korur_link_rel_ekler():
    sonuc = temiz_html('<h2>B</h2><p><strong>k</strong> <a href="https://e.com" onclick="x">l</a></p>')
    assert "<h2>B</h2>" in sonuc and "<strong>k</strong>" in sonuc
    assert 'href="https://e.com"' in sonuc and "onclick" not in sonuc and "noopener" in sonuc


def test_temiz_html_javascript_linkini_siler():
    assert "javascript" not in temiz_html('<a href="javascript:alert(1)">x</a>')


def test_temiz_html_none_bos_string():
    assert temiz_html(None) == ""
