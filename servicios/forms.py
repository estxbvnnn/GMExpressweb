from django import forms
from .models import Servicio, TipoServicio

class TipoServicioForm(forms.ModelForm):
    class Meta:
        model = TipoServicio
        fields = ["nombre", "descripcion"]
        widgets = {
            "nombre": forms.TextInput(attrs={"class": "form-control"}),
            "descripcion": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }

class ServicioForm(forms.ModelForm):
    class Meta:
        model = Servicio
        fields = ["nombre", "tipo", "precio", "descripcion", "estado"]
        widgets = {
            "nombre": forms.TextInput(attrs={"class": "form-control"}),
            "tipo": forms.Select(attrs={"class": "form-select"}),
            "precio": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
            "descripcion": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "estado": forms.Select(attrs={"class": "form-select"}),
        }

    def clean_precio(self):
        p = self.cleaned_data.get("precio")
        if p is None or p < 0:
            raise forms.ValidationError("Precio inválido.")
        return p
