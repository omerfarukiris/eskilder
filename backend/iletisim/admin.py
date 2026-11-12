from django.contrib import admin
from unfold.admin import ModelAdmin

from .models import IletisimMesaji


@admin.register(IletisimMesaji)
class IletisimMesajiAdmin(ModelAdmin):
    list_display = ["ad_soyad", "konu", "eposta", "olusturma", "durum"]
    list_filter = ["durum", "konu"]
    search_fields = ["ad_soyad", "eposta", "mesaj"]
    readonly_fields = ["ad_soyad", "eposta", "telefon", "konu", "mesaj", "kvkk_onay", "olusturma"]
    fields = ["durum", "ad_soyad", "eposta", "telefon", "konu", "mesaj", "kvkk_onay", "olusturma"]

    def has_add_permission(self, request):
        return False

    def change_view(self, request, object_id, form_url="", extra_context=None):
        if request.method == "GET":
            IletisimMesaji.objects.filter(pk=object_id, durum="yeni").update(durum="okundu")
        return super().change_view(request, object_id, form_url, extra_context)
