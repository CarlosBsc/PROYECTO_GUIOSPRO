from django.urls import path
from .views import inicio
from .views import inicio, nueva_evaluacion, panel

app_name = "evaluacion"

urlpatterns = [
    path("", inicio, name="inicio"),
    path("nueva-evaluacion/", nueva_evaluacion, name="nueva_evaluacion"),
    path("panel/", panel, name="panel"),
    ]
