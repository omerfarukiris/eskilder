from django.db.models import Prefetch
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_control
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from . import serializers as s
from .models import Destekci, Duyuru, Etkinlik, SiteAyarlari

onbellek = cache_control(public=True, max_age=60)


class Sayfalama(PageNumberPagination):
    page_size = 9
    page_query_param = "sayfa"


def gorunur_duyurular():
    """Yayında olan ve yayın tarihi gelmiş duyurular. OG sayfaları da bu kuralı kullanır."""
    return Duyuru.objects.filter(yayinda=True, yayin_tarihi__lte=timezone.now())


def gorunur_etkinlikler():
    return Etkinlik.objects.filter(yayinda=True)


@method_decorator(onbellek, name="dispatch")
class DuyuruViewSet(viewsets.ReadOnlyModelViewSet):
    lookup_field = "slug"
    pagination_class = Sayfalama

    def get_queryset(self):
        return gorunur_duyurular().prefetch_related("fotograflar")

    def get_serializer_class(self):
        return s.DuyuruDetaySerializer if self.action == "retrieve" else s.DuyuruListeSerializer


@method_decorator(onbellek, name="dispatch")
class EtkinlikViewSet(viewsets.ReadOnlyModelViewSet):
    lookup_field = "slug"
    pagination_class = Sayfalama

    def get_queryset(self):
        sorgu = gorunur_etkinlikler().prefetch_related("fotograflar")
        if self.action != "list":
            return sorgu
        zaman = self.request.query_params.get("zaman")
        simdi = timezone.now()
        if zaman == "yaklasan":
            return sorgu.filter(baslangic__gte=simdi).order_by("baslangic")
        if zaman == "gecmis":
            return sorgu.filter(baslangic__lt=simdi).order_by("-baslangic")
        return sorgu

    def get_serializer_class(self):
        return s.EtkinlikDetaySerializer if self.action == "retrieve" else s.EtkinlikListeSerializer


@method_decorator(onbellek, name="dispatch")
class DestekciViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = s.DestekciSerializer
    pagination_class = None

    def get_queryset(self):
        return Destekci.objects.filter(yayin_izni=True)


@onbellek
@api_view(["GET"])
def ayarlar(request):
    return Response(s.AyarlarSerializer(SiteAyarlari.yukle(), context={"request": request}).data)
