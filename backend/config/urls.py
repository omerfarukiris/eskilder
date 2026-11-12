from django.contrib import admin
from django.urls import path

from saglik.views import saglik

urlpatterns = [
    path("api/saglik/", saglik, name="saglik"),
    path("yonetim/", admin.site.urls),
]
