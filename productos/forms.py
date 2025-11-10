from django import forms
from .models import Producto, CategoriaProducto

class CategoriaProductoForm(forms.ModelForm):
    class Meta:
        model = CategoriaProducto
        fields = ["nombre", "descripcion"]
        widgets = {
            "nombre": forms.TextInput(attrs={"class": "form-control"}),
            "descripcion": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ["nombre", "categoria", "precio", "descripcion", "stock", "unidad_medida"]
        widgets = {
            "nombre": forms.TextInput(attrs={"class": "form-control"}),
            "categoria": forms.Select(attrs={"class": "form-select"}),
            "precio": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
            "descripcion": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "stock": forms.NumberInput(attrs={"class": "form-control", "min": 0}),
            "unidad_medida": forms.Select(attrs={"class": "form-select"}),
        }

    def clean_precio(self):
        p = self.cleaned_data.get("precio")
        if p is None or p < 0:
            raise forms.ValidationError("Precio inválido.")
        return p

    def clean_stock(self):
        s = self.cleaned_data.get("stock")
        if s is None or s < 0:
            raise forms.ValidationError("Stock inválido.")
        return s
