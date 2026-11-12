from rest_framework import serializers

from .models import (
    Destekci, Dokuman, Duyuru, DuyuruFotografi, EtkiRakami, Etkinlik, EtkinlikFotografi, SiteAyarlari,
    YonetimKuruluUyesi,
)


class FotografSerializer(serializers.Serializer):
    gorsel = serializers.ImageField()
    aciklama = serializers.CharField()


class DuyuruListeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Duyuru
        fields = ["baslik", "slug", "ozet", "kapak", "yayin_tarihi", "one_cikan"]


class DuyuruDetaySerializer(DuyuruListeSerializer):
    fotograflar = FotografSerializer(many=True, read_only=True)

    class Meta(DuyuruListeSerializer.Meta):
        fields = DuyuruListeSerializer.Meta.fields + ["icerik", "fotograflar"]


class EtkinlikListeSerializer(serializers.ModelSerializer):
    tur_adi = serializers.CharField(source="get_tur_display", read_only=True)

    class Meta:
        model = Etkinlik
        fields = ["tur", "tur_adi", "baslik", "slug", "baslangic", "yer", "kapak"]


class EtkinlikDetaySerializer(EtkinlikListeSerializer):
    fotograflar = FotografSerializer(many=True, read_only=True)

    class Meta(EtkinlikListeSerializer.Meta):
        fields = EtkinlikListeSerializer.Meta.fields + ["aciklama", "fotograflar"]


class DestekciSerializer(serializers.ModelSerializer):
    class Meta:
        model = Destekci
        fields = ["ad", "tur", "logo", "not_metni"]


class AyarlarSerializer(serializers.ModelSerializer):
    rakamlar = serializers.SerializerMethodField()
    kurul = serializers.SerializerMethodField()
    dokumanlar = serializers.SerializerMethodField()

    class Meta:
        model = SiteAyarlari
        exclude = ["id"]

    def _dosya(self, alan):
        return self.context["request"].build_absolute_uri(alan.url) if alan else None

    def get_rakamlar(self, _):
        return [{"etiket": r.etiket, "deger": r.deger} for r in EtkiRakami.objects.all()]

    def get_kurul(self, _):
        return [{"ad_soyad": k.ad_soyad, "gorev": k.gorev, "fotograf": self._dosya(k.fotograf)}
                for k in YonetimKuruluUyesi.objects.all()]

    def get_dokumanlar(self, _):
        return [{"baslik": d.baslik, "dosya": self._dosya(d.dosya)} for d in Dokuman.objects.filter(yayinda=True)]
