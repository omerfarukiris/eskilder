from django.contrib import admin
from django.core.exceptions import PermissionDenied, ValidationError
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import path, reverse
from django.utils.html import format_html
from django.views.decorators.http import require_POST
from unfold.admin import ModelAdmin, TabularInline
from unfold.contrib.forms.widgets import WysiwygWidget

from ortak.gorsel import GorselHatasi, kucult

from .models import (
    Destekci, Dokuman, Duyuru, DuyuruFotografi, EtkiRakami, Etkinlik, EtkinlikFotografi, SiteAyarlari,
    YonetimKuruluUyesi,
)

GORSEL_JS = ("icerik/admin/gorsel_kucult.js",)


def onizleme(alan, yukseklik=48):
    if not alan:
        return "—"
    return format_html('<img src="{}" style="height:{}px;width:auto;border-radius:6px;object-fit:cover">', alan.url, yukseklik)


class TemelAdmin(ModelAdmin):
    zengin_alanlar = ()
    warn_unsaved_form = True

    class Media:
        js = GORSEL_JS

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        if db_field.name in self.zengin_alanlar:
            kwargs["widget"] = WysiwygWidget
        return super().formfield_for_dbfield(db_field, request, **kwargs)


class GaleriYuklemeMixin:
    """Fotoğrafları tek tek ayrı isteklerle yükler (Vercel 4,5 MB istek sınırı)."""
    foto_modeli = None
    foto_fk = None
    change_form_after_template = "icerik/admin/galeri_yukle.html"

    def get_urls(self):
        ozel = [path("<int:pk>/galeri-yukle/", self.admin_site.admin_view(self.galeri_yukle),
                     name=f"{self.model._meta.app_label}_{self.model._meta.model_name}_galeri_yukle")]
        return ozel + super().get_urls()

    def galeri_yukle(self, request, pk):
        return require_POST(self._galeri_yukle)(request, pk)

    def _galeri_yukle(self, request, pk):
        nesne = get_object_or_404(self.model, pk=pk)
        if not self.has_change_permission(request, nesne):
            raise PermissionDenied
        dosya = request.FILES.get("dosya")
        if not dosya:
            return JsonResponse({"hata": "Dosya seçilmedi."}, status=400)
        try:
            kucuk = kucult(dosya)
        except (GorselHatasi, ValidationError) as hata:
            return JsonResponse({"hata": " ".join(hata.messages)}, status=400)
        sira = self.foto_modeli.objects.filter(**{self.foto_fk: nesne}).count()
        foto = self.foto_modeli.objects.create(**{self.foto_fk: nesne}, gorsel=kucuk, sira=sira)
        return JsonResponse({"id": foto.pk, "gorsel": foto.gorsel.url})

    def render_change_form(self, request, context, *args, obj=None, **kwargs):
        if obj is not None:
            context["galeri_yukle_url"] = reverse(
                f"admin:{self.model._meta.app_label}_{self.model._meta.model_name}_galeri_yukle", args=[obj.pk])
        return super().render_change_form(request, context, *args, obj=obj, **kwargs)


class FotografInline(TabularInline):
    extra = 0
    ordering_field = "sira"
    hide_ordering_field = True
    fields = ["onizleme", "gorsel", "aciklama", "sira"]
    readonly_fields = ["onizleme"]

    @admin.display(description="Önizleme")
    def onizleme(self, obj):
        return onizleme(obj.gorsel, 64)


class DuyuruFotografiInline(FotografInline):
    model = DuyuruFotografi


class EtkinlikFotografiInline(FotografInline):
    model = EtkinlikFotografi


@admin.register(Duyuru)
class DuyuruAdmin(GaleriYuklemeMixin, TemelAdmin):
    foto_modeli, foto_fk = DuyuruFotografi, "duyuru"
    zengin_alanlar = ("icerik",)
    list_display = ["kapak_onizleme", "baslik", "yayin_tarihi", "yayinda", "one_cikan"]
    list_display_links = ["kapak_onizleme", "baslik"]
    list_filter = ["yayinda", "one_cikan"]
    search_fields = ["baslik", "ozet"]
    fields = ["baslik", "ozet", "kapak", "icerik", "yayin_tarihi", "yayinda", "one_cikan"]
    inlines = [DuyuruFotografiInline]

    @admin.display(description="Kapak")
    def kapak_onizleme(self, obj):
        return onizleme(obj.kapak)


@admin.register(Etkinlik)
class EtkinlikAdmin(GaleriYuklemeMixin, TemelAdmin):
    foto_modeli, foto_fk = EtkinlikFotografi, "etkinlik"
    zengin_alanlar = ("aciklama",)
    list_display = ["kapak_onizleme", "baslik", "tur", "baslangic", "yer", "yayinda"]
    list_display_links = ["kapak_onizleme", "baslik"]
    list_filter = ["tur", "yayinda"]
    search_fields = ["baslik", "yer"]
    fields = ["tur", "baslik", "baslangic", "yer", "kapak", "aciklama", "yayinda"]
    inlines = [EtkinlikFotografiInline]

    @admin.display(description="Kapak")
    def kapak_onizleme(self, obj):
        return onizleme(obj.kapak)


@admin.register(Destekci)
class DestekciAdmin(TemelAdmin):
    list_display = ["logo_onizleme", "ad", "tur", "yayin_izni", "not_metni", "sira"]
    list_display_links = ["logo_onizleme", "ad"]
    list_filter = ["yayin_izni", "tur"]
    search_fields = ["ad"]
    ordering_field = "sira"
    hide_ordering_field = True
    fields = ["ad", "tur", "logo", "not_metni", "yayin_izni"]

    @admin.display(description="Logo")
    def logo_onizleme(self, obj):
        return onizleme(obj.logo)


@admin.register(EtkiRakami)
class EtkiRakamiAdmin(TemelAdmin):
    list_display = ["deger", "etiket", "sira"]
    ordering_field = "sira"
    hide_ordering_field = True
    fields = ["deger", "etiket"]


@admin.register(YonetimKuruluUyesi)
class YonetimKuruluAdmin(TemelAdmin):
    list_display = ["foto_onizleme", "ad_soyad", "gorev", "sira"]
    list_display_links = ["foto_onizleme", "ad_soyad"]
    ordering_field = "sira"
    hide_ordering_field = True
    fields = ["ad_soyad", "gorev", "fotograf"]

    @admin.display(description="Fotoğraf")
    def foto_onizleme(self, obj):
        return onizleme(obj.fotograf)


@admin.register(Dokuman)
class DokumanAdmin(TemelAdmin):
    list_display = ["baslik", "dosya", "yayinda", "sira"]
    ordering_field = "sira"
    hide_ordering_field = True
    fields = ["baslik", "dosya", "yayinda"]


@admin.register(SiteAyarlari)
class SiteAyarlariAdmin(TemelAdmin):
    zengin_alanlar = ("hakkimizda_metni", "burs_metni", "kvkk_metni")
    fieldsets = [
        ("Kimlik", {"fields": ["resmi_ad", "kisa_ad", "slogan", "logo", "hero_gorsel", "hero_metin"]}),
        ("İletişim", {"fields": ["telefon", "whatsapp", "eposta", "adres", "harita_embed_url"]}),
        ("Bağış", {"fields": ["iban", "hesap_sahibi", "banka", "destek_ol_metni"]}),
        ("Sayfa metinleri", {"fields": ["hakkimizda_metni", "burs_metni", "kvkk_metni"]}),
        ("Sosyal medya", {"fields": ["facebook", "instagram", "x", "youtube"]}),
    ]

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        return redirect(reverse("admin:icerik_siteayarlari_change", args=[SiteAyarlari.yukle().pk]))
