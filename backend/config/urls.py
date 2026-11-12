from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import SimpleRouter

from icerik import api as icerik_api
from iletisim.api import iletisim
from saglik.views import saglik

router = SimpleRouter()
router.register("duyurular", icerik_api.DuyuruViewSet, basename="duyuru")
router.register("etkinlikler", icerik_api.EtkinlikViewSet, basename="etkinlik")
router.register("destekciler", icerik_api.DestekciViewSet, basename="destekci")

urlpatterns = [
    path("api/saglik/", saglik, name="saglik"),
    path("api/iletisim/", iletisim, name="iletisim"),
    path("api/ayarlar/", icerik_api.ayarlar, name="ayarlar"),
    path("api/", include(router.urls)),
    path("yonetim/", admin.site.urls),
]
