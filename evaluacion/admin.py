
from django.contrib import admin
from .models import Organizacion, Categoria, Evaluacion


@admin.register(Organizacion)
class OrganizacionAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre")
    search_fields = ("nombre",)


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre")
    search_fields = ("nombre",)


@admin.register(Evaluacion)
class EvaluacionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "software",
        "organizacion",
        "categoria",
        "usuario",
        "fecha_creacion",
    )

    list_filter = ("categoria", "organizacion", "fecha_creacion")
    search_fields = ("software", "organizacion__nombre")
