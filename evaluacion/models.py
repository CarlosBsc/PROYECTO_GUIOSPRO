
from django.db import models
from django.contrib.auth.models import User


# ==========================================
# MODELO: ORGANIZACIÓN
# ==========================================

class Organizacion(models.Model):
    nombre = models.CharField(max_length=150, unique=True)

    class Meta:
        verbose_name = "Organización"
        verbose_name_plural = "Organizaciones"
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre


# ==========================================
# MODELO: CATEGORÍA DE SOFTWARE
# ==========================================

class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre


# ==========================================
# MODELO: EVALUACIÓN
# ==========================================

class Evaluacion(models.Model):
    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="evaluaciones"
    )

    organizacion = models.ForeignKey(
        Organizacion,
        on_delete=models.PROTECT,
        related_name="evaluaciones"
    )

    software = models.CharField(max_length=150)

    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.PROTECT,
        related_name="evaluaciones"
    )

    descripcion = models.TextField(
        blank=True
    )

    fecha_creacion = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        verbose_name = "Evaluación"
        verbose_name_plural = "Evaluaciones"
        ordering = ["-fecha_creacion"]

    def __str__(self):
        return f"{self.software} - {self.organizacion.nombre}"

