from django.contrib import admin
from django.urls import re_path, include

urlpatterns = [
    re_path("admin", admin.site.urls),
    re_path("", include("api.urls")),
]
