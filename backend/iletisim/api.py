from rest_framework import serializers, status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from ortak.ip import istemci_ip

from .models import IletisimMesaji
from .servis import bildirim_gonder, sinir_asildi_mi

SINIR_MESAJI = "Çok fazla mesaj gönderildi. Lütfen bir saat sonra tekrar deneyin."


class IletisimSerializer(serializers.ModelSerializer):
    web_sitesi = serializers.CharField(required=False, allow_blank=True, write_only=True)
    kvkk_onay = serializers.BooleanField()

    class Meta:
        model = IletisimMesaji
        fields = ["ad_soyad", "eposta", "telefon", "konu", "mesaj", "kvkk_onay", "web_sitesi"]
        extra_kwargs = {
            "ad_soyad": {"error_messages": {"blank": "Ad soyad zorunludur.", "required": "Ad soyad zorunludur."}},
            "eposta": {"error_messages": {"invalid": "Geçerli bir e-posta adresi girin.",
                                          "blank": "E-posta zorunludur.", "required": "E-posta zorunludur."}},
            "mesaj": {"error_messages": {"blank": "Mesaj zorunludur.", "required": "Mesaj zorunludur."}},
            "konu": {"error_messages": {"invalid_choice": "Lütfen bir konu seçin.", "required": "Lütfen bir konu seçin."}},
        }

    def validate_kvkk_onay(self, deger):
        if not deger:
            raise serializers.ValidationError("Devam etmek için KVKK aydınlatma metnini onaylamanız gerekir.")
        return deger

    def create(self, veri):
        veri.pop("web_sitesi", None)
        return super().create(veri)


@api_view(["POST"])
def iletisim(request):
    if str(request.data.get("web_sitesi", "")).strip():
        return Response({"tamam": True}, status=status.HTTP_201_CREATED)
    if sinir_asildi_mi(istemci_ip(request)):
        return Response({"hata": SINIR_MESAJI}, status=status.HTTP_429_TOO_MANY_REQUESTS)
    seri = IletisimSerializer(data=request.data)
    if not seri.is_valid():
        return Response(seri.errors, status=status.HTTP_400_BAD_REQUEST)
    bildirim_gonder(seri.save())
    return Response({"tamam": True}, status=status.HTTP_201_CREATED)
