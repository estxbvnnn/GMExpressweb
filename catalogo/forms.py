from django import forms
from django.contrib.auth.models import User
import re
from django.contrib.auth.forms import AuthenticationForm

class RegisterForm(forms.Form):
    first_name = forms.CharField(label="Nombre", max_length=30, widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Nombre"}))
    last_name = forms.CharField(label="Apellido", max_length=30, widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Apellido"}))
    email = forms.EmailField(label="Correo", widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "correo@ejemplo.com"}))
    password1 = forms.CharField(label="Contraseña", widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Contraseña"}), min_length=8)
    password2 = forms.CharField(label="Confirmar contraseña", widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Confirmar contraseña"}))

    def clean_email(self):
        email = self.cleaned_data.get("email").lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("Ya existe una cuenta con este correo.")
        return email

    def clean_password1(self):
        p = self.cleaned_data.get("password1", "")
        if not re.search(r"[A-Z]", p):
            raise forms.ValidationError("La contraseña debe contener al menos una letra mayúscula.")
        if not re.search(r"[^A-Za-z0-9]", p):
            raise forms.ValidationError("La contraseña debe contener al menos un carácter especial.")
        return p

    def clean(self):
        cleaned = super().clean()
        p1 = cleaned.get("password1")
        p2 = cleaned.get("password2")
        if p1 and p2 and p1 != p2:
            self.add_error("password2", "Las contraseñas no coinciden.")
        return cleaned

class LoginForm(AuthenticationForm):
    username = forms.EmailField(
        widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "tu@ejemplo.com", "autofocus": True}),
        label="Correo",
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Contraseña"}),
        label="Contraseña",
    )
