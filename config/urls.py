from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),

    # Registro, login y recuperación de contraseña
    path("accounts/", include("allauth.urls")),

    # Sistema GUIOSPRO
    path("", include("evaluacion.urls")),
]