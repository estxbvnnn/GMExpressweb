from django.shortcuts import render, Http404
from .data import CATALOGOS

def index(request):
    contexto = {"categorias": CATALOGOS, "empresa": empresa_info()}
    return render(request, "catalogo/index.html", contexto)

def categoria(request, slug):
    categoria = next((c for c in CATALOGOS if c["slug"] == slug), None)
    if not categoria:
        raise Http404("Categoría no encontrada")
    contexto = {"categoria": categoria, "empresa": empresa_info()}
    return render(request, "catalogo/categoria.html", contexto)

def producto(request, cat_slug, prod_slug):
    categoria = next((c for c in CATALOGOS if c["slug"] == cat_slug), None)
    if not categoria:
        raise Http404("Categoría no encontrada")
    producto = next((p for p in categoria["productos"] if p["slug"] == prod_slug), None)
    if not producto:
        raise Http404("Producto no encontrado")
    contexto = {"categoria": categoria, "producto": producto, "empresa": empresa_info()}
    return render(request, "catalogo/producto.html", contexto)

def about(request):
    contexto = {"empresa": empresa_info()}
    return render(request, "catalogo/about.html", contexto)

def empresa_info():
    return {
        "nombre": "GM Express",
        "historia": "GM Express nace para ofrecer soluciones alimentarias eficientes y de calidad en instituciones y eventos.",
        "mision": "Entregar alimentos saludables y servicios profesionales que faciliten la alimentación institucional y de eventos.",
        "vision": "Ser referente en gestión alimentaria en colegios, universidades y eventos en Chile.",
        "valores": ["Calidad", "Responsabilidad", "Sostenibilidad", "Compromiso"],
        "contactos": {"telefono": "+56 9 0000 0000", "email": "contacto@gmexpress.cl", "direccion": "Santiago, Chile"},
        "redes": {"facebook": "#", "instagram": "#", "twitter": "#"},
    }
