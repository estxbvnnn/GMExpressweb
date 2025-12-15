from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db import transaction
from decimal import Decimal, ROUND_HALF_UP
from .models import Producto, CategoriaProducto, Compra, CompraItem
from .forms import ProductoForm, CategoriaProductoForm
from django.contrib import messages

# Vistas existentes...

IVA_RATE = Decimal("0.19")
MONEY_PLACES = Decimal("0.01")

def _money(value):
    return value.quantize(MONEY_PLACES, rounding=ROUND_HALF_UP)

def _iva_breakdown(subtotal):
    subtotal = _money(subtotal)
    iva = _money(subtotal * IVA_RATE)
    return subtotal, iva, _money(subtotal + iva)

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

def _cart_qty(cart, prod_id):
    value = cart.get(str(prod_id), 0)
    try:
        return int(value)
    except (TypeError, ValueError):
        return 0

@login_required
def cart_add(request, pk):
    if request.method != "POST":
        return redirect("productos:list")
    qty_raw = request.POST.get("cantidad") or request.POST.get("qty")
    try:
        qty = int(qty_raw)
    except (TypeError, ValueError):
        qty = 0
    if qty <= 0:
        messages.error(request, "Cantidad inválida.")
        return redirect("productos:list")
    product = get_object_or_404(Producto, pk=pk)
    cart = _get_cart(request)
    cart[str(product.pk)] = _cart_qty(cart, product.pk) + qty
    request.session.modified = True
    messages.success(request, f"{qty} × {product.nombre} añadidos al carrito.")
    return redirect("productos:cart")

@login_required
def cart_view(request):
    cart = _get_cart(request)
    ids = [int(pk) for pk in cart.keys() if _cart_qty(cart, pk) > 0]
    productos = Producto.objects.filter(id__in=ids).select_related("categoria") if ids else Producto.objects.none()
    items = []
    subtotal_acum = Decimal("0.00")
    for prod in productos:
        qty = _cart_qty(cart, prod.id)
        if qty <= 0:
            continue
        line_total = prod.precio * qty
        subtotal_acum += line_total
        items.append({
            "prod": prod,
            "qty": qty,
            "precio": prod.precio,
            "subtotal": _money(line_total),
        })
    subtotal, iva, total = _iva_breakdown(subtotal_acum)
    return render(request, "productos/cart.html", {
        "items": items,
        "subtotal": subtotal,
        "iva": iva,
        "total": total,
        "iva_rate": int(IVA_RATE * 100),
        "item_count": sum(item["qty"] for item in items),
    })

@login_required
def cart_checkout(request):
    if request.method != "POST":
        return redirect("productos:cart")
    cart = _get_cart(request)
    if not cart:
        messages.error(request, "El carrito está vacío.")
        return redirect("productos:cart")
    ids = [int(pk) for pk in cart.keys() if _cart_qty(cart, pk) > 0]
    if not ids:
        messages.error(request, "El carrito no contiene cantidades válidas.")
        return redirect("productos:cart")
    with transaction.atomic():
        productos = list(Producto.objects.select_for_update().filter(id__in=ids))
        if len(productos) != len(ids):
            messages.error(request, "Algún producto ya no existe.")
            return redirect("productos:cart")
        subtotal_acum = Decimal("0.00")
        for prod in productos:
            qty = _cart_qty(cart, prod.id)
            if qty <= 0 or qty > prod.stock:
                messages.error(request, f"Stock insuficiente para {prod.nombre}.")
                return redirect("productos:cart")
            subtotal_acum += prod.precio * qty
        subtotal, iva, total = _iva_breakdown(subtotal_acum)
        compra = Compra.objects.create(usuario=request.user, total=total)
        for prod in productos:
            qty = _cart_qty(cart, prod.id)
            prod.stock -= qty
            prod.save(update_fields=["stock"])
            CompraItem.objects.create(
                compra=compra,
                producto=prod,
                cantidad=qty,
                precio_unitario=prod.precio,
            )
        compra.total = total
        compra.save(update_fields=["total"])
    request.session["cart"] = {}
    request.session.modified = True
    messages.success(
        request,
        "Compra realizada. Subtotal ${}, IVA ({} %) ${}, Total ${}.".format(
            format(subtotal, ",.2f"),
            int(IVA_RATE * 100),
            format(iva, ",.2f"),
            format(total, ",.2f"),
        ),
    )
    return redirect("productos:history")

@login_required
def purchase_history(request):
    compras = (
        Compra.objects.filter(usuario=request.user)
        .prefetch_related("items__producto__categoria")
        .order_by("-creada_en")
    )
    historial = []
    for compra in compras:
        detalle = []
        subtotal_acum = Decimal("0.00")
        total_items = 0
        for item in compra.items.all():
            line_total = item.precio_unitario * item.cantidad
            subtotal_acum += line_total
            total_items += item.cantidad
            detalle.append({
                "producto": item.producto,
                "cantidad": item.cantidad,
                "precio_unitario": item.precio_unitario,
                "subtotal": _money(line_total),
                "categoria": getattr(item.producto.categoria, "nombre", ""),
            })
        subtotal, iva, total = _iva_breakdown(subtotal_acum)
        historial.append({
            "compra": compra,
            "items": detalle,
            "subtotal": subtotal,
            "iva": iva,
            "total": total,
            "total_items": total_items,
        })
    return render(request, "productos/history.html", {
        "compras": compras,
        "historial": historial,
        "iva_rate": int(IVA_RATE * 100),
    })
