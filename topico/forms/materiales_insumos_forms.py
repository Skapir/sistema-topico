from django import forms
from ..models import MaterialesInsumos  # Importar desde la carpeta de modelos


class MaterialesInsumosForm(forms.ModelForm):
    class Meta:
        model = MaterialesInsumos
        fields = ["descripcion", "fecha_vencimiento", "unidad_medida", "stock_actual"]
        widgets = {
            "descripcion": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Ingrese descripción"}
            ),
            "fecha_vencimiento": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
            "unidad_medida": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ingrese unidad de medida",
                }
            ),
            "stock_actual": forms.NumberInput(
                attrs={"class": "form-control", "placeholder": "Ingrese stock actual"}
            ),
        }
