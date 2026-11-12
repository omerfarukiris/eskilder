from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path
from rest_framework.routers import SimpleRouter

from icerik import api as icerik_api
from icerik import og, sitemap
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
    re_path(r"^duyurular/(?P<slug>[-a-z0-9_]+)/?$", og.duyuru_sayfasi, name="duyuru_sayfasi"),
    re_path(r"^etkinlikler/(?P<slug>[-a-z0-9_]+)/?$", og.etkinlik_sayfasi, name="etkinlik_sayfasi"),
    path("sitemap.xml", sitemap.sitemap, name="sitemap"),
    path("robots.txt", sitemap.robots, name="robots"),
]

if settings.DEBUG and settings.STORAGES["default"]["BACKEND"].endswith("FileSystemStorage"):
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
