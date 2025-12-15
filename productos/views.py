from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db import transaction
from django.db.models import F
from decimal import Decimal
from .models import Producto, CategoriaProducto, Compra, CompraItem
from .forms import ProductoForm, CategoriaProductoForm
from django.contrib import messages

# Vistas existentes...

def product_list(request):
    qs = Producto.objects.filter().order_by("categoria__nombre", "nombre")
    return render(request, "productos/list.html", {"productos": qs})

def product_detail(request, pk):
    p = get_object_or_404(Producto, pk=pk)
    return render(request, "productos/detail.html", {"producto": p})

@login_required
def product_create(request):
    if request.method == "POST":
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Producto creado.")
            return redirect("productos:list")
    else:
        form = ProductoForm()
    return render(request, "productos/form.html", {"form": form, "action": "Crear"})

@login_required
def product_update(request, pk):
    p = get_object_or_404(Producto, pk=pk)
    if request.method == "POST":
        form = ProductoForm(request.POST, instance=p)
        if form.is_valid():
            form.save()
            messages.success(request, "Producto actualizado.")
            return redirect("productos:detail", pk=p.pk)
    else:
        form = ProductoForm(instance=p)
    return render(request, "productos/form.html", {"form": form, "action": "Editar"})

@login_required
def product_delete(request, pk):
    p = get_object_or_404(Producto, pk=pk)
    if request.method == "POST":
        p.delete()
        messages.success(request, "Producto eliminado.")
        return redirect("productos:list")
    return render(request, "productos/form.html", {"confirm_delete": True, "obj": p, "action": "Eliminar"})

# Dashboard de gestión (solo staff)
staff_required = user_passes_test(lambda u: u.is_active and u.is_staff)

@staff_required
def manage_index(request):
    total = Producto.objects.count()
    categorias = CategoriaProducto.objects.count()
    recientes = Producto.objects.order_by("-id")[:6]
    all_products = Producto.objects.order_by("categoria__nombre", "nombre")  # lista completa para gestión
    return render(request, "productos/manage.html", {
        "total": total,
        "categorias": categorias,
        "recientes": recientes,
        "all_products": all_products,
    })

# Categorías
def categoria_list(request):
    qs = CategoriaProducto.objects.all().order_by("nombre")
    return render(request, "productos/categoria_list.html", {"categorias": qs})

@login_required
def categoria_create(request):
    if request.method == "POST":
        form = CategoriaProductoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Categoría creada.")
            return redirect("productos:categoria_list")
    else:
        form = CategoriaProductoForm()
    return render(request, "productos/categoria_form.html", {"form": form, "action": "Crear categoría"})

def categoria_detail(request, pk):
    c = get_object_or_404(CategoriaProducto, pk=pk)
    return render(request, "productos/categoria_detail.html", {"categoria": c})

@staff_required
def categoria_update(request, pk):
    c = get_object_or_404(CategoriaProducto, pk=pk)
    if request.method == "POST":
        form = CategoriaProductoForm(request.POST, instance=c)
        if form.is_valid():
            form.save()
            messages.success(request, "Categoría actualizada.")
            return redirect("productos:categoria_list")
    else:
        form = CategoriaProductoForm(instance=c)
    return render(request, "productos/categoria_form.html", {"form": form, "action": "Editar categoría"})

@staff_required
def categoria_delete(request, pk):
    c = get_object_or_404(CategoriaProducto, pk=pk)
    if request.method == "POST":
        c.delete()
        messages.success(request, "Categoría eliminada.")
        return redirect("productos:categoria_list")
    # Reusar plantilla de confirmación simple
    return render(request, "productos/categoria_form.html", {"confirm_delete": True, "obj": c, "action": "Eliminar categoría"})

def _get_cart(request):
    cart = request.session.get("cart", {})
    request.session["cart"] = cart
    return cart

@login_required
def cart_add(request, pk):
    if request.method != "POST":
        return redirect("productos:list")
    qty = request.POST.get("cantidad") or request.POST.get("qty")
    try:
        qty = int(qty)
    except (TypeError, ValueError):
        qty = 0
    if qty <= 0:
        messages.error(request, "Cantidad inválida.")
        return redirect("productos:list")
    product = get_object_or_404(Producto, pk=pk)
    cart = _get_cart(request)
    cart[str(pk)] = cart.get(str(pk), 0) + qty
    request.session.modified = True
    messages.success(request, f"{product.nombre} añadido al carrito.")
    return redirect("productos:list")

@login_required
def cart_view(request):
    cart = _get_cart(request)
    ids = [int(k) for k in cart.keys()]
    productos = Producto.objects.filter(id__in=ids)
    items = []
    total = Decimal("0.00")
    for prod in productos:
        qty = cart.get(str(prod.id), 0)
        subtotal = prod.precio * qty
        total += subtotal
        items.append({"prod": prod, "qty": qty, "subtotal": subtotal})
    return render(request, "productos/cart.html", {"items": items, "total": total})

@login_required
def cart_checkout(request):
    if request.method != "POST":
        return redirect("productos:cart")
    cart = _get_cart(request)
    if not cart:
        messages.error(request, "El carrito está vacío.")
        return redirect("productos:cart")
    ids = [int(k) for k in cart.keys()]
    with transaction.atomic():
        productos = Producto.objects.select_for_update().filter(id__in=ids)
        if productos.count() != len(ids):
            messages.error(request, "Algún producto ya no existe.")
            return redirect("productos:cart")
        for prod in productos:
            qty = cart[str(prod.id)]
            if qty <= 0 or qty > prod.stock:
                messages.error(request, f"Stock insuficiente para {prod.nombre}.")
                return redirect("productos:cart")
        compra = Compra.objects.create(usuario=request.user, total=Decimal("0.00"))
        total = Decimal("0.00")
        for prod in productos:
            qty = cart[str(prod.id)]
            prod.stock = F("stock") - qty
            prod.save(update_fields=["stock"])
            CompraItem.objects.create(
                compra=compra,
                producto=prod,
                cantidad=qty,
                precio_unitario=prod.precio,
            )
            total += prod.precio * qty
        compra.total = total
        compra.save(update_fields=["total"])
    request.session["cart"] = {}
    request.session.modified = True
    messages.success(request, f"Compra realizada. Total ${total}.")
    return redirect("productos:history")

@login_required
def purchase_history(request):
    compras = (
        Compra.objects.filter(usuario=request.user)
        .prefetch_related("items__producto")
        .order_by("-creada_en")
    )
    return render(request, "productos/history.html", {"compras": compras})
