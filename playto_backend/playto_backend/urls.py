from django.contrib import admin
from django.urls import path, include
from core.views import home   # 👈 IMPORT HOME VIEW

urlpatterns = [
    path("", home),            # 👈 ROOT URL FIX
    path("admin/", admin.site.urls),
    path("api/", include("core.urls")),
]
