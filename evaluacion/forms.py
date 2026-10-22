
from django import forms
from .models import Evaluacion


class EvaluacionForm(forms.ModelForm):

    class Meta:
        model = Evaluacion

        fields = [
            "organizacion",
            "software",
            "categoria",
            "descripcion",
        ]

        widgets = {
            "organizacion": forms.Select(
                attrs={
                    "class": "form-select evaluation-input",
                    "id": "organizacion",
                }
            ),

            "software": forms.TextInput(
                attrs={
                    "class": "form-control evaluation-input",
                    "id": "software",
                    "placeholder": "Ej. Odoo ERP",
                }
            ),

            "categoria": forms.Select(
                attrs={
                    "class": "form-select evaluation-input",
                    "id": "categoria",
                }
            ),

            "descripcion": forms.Textarea(
                attrs={
                    "class": "form-control evaluation-input",
                    "id": "descripcion",
                    "rows": 3,
                    "placeholder": "¿Qué necesidad busca resolver?",
                }
            ),
        }
