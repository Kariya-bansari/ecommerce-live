# ============================================================
# FILE: store/views.py
# ============================================================
import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.models import User
from adminpanel.models import Product  # ✅ reads from adminpanel_product table
from .models import Cart, Wishlist, Order, OrderItem


# ─── PRODUCT LIST ────────────────────────────────────────────────────────────
def product_list(request):
    products = Product.objects.all()
    cart_product_ids = []
    wishlist_product_ids = []
    if request.user.is_authenticated:
        cart_product_ids = list(
            Cart.objects.filter(user=request.user).values_list('product_id', flat=True)
        )
        wishlist_product_ids = list(
            Wishlist.objects.filter(user=request.user).values_list('product_id', flat=True)
        )
    return render(request, "product_list.html", {
        "products": products,
        "cart_product_ids": cart_product_ids,
        "wishlist_product_ids": wishlist_product_ids,
    })


# ─── AJAX: TOGGLE CART ───────────────────────────────────────────────────────
@require_POST
def toggle_cart_ajax(request, id):
    try:
        if not request.user.is_authenticated:
            return JsonResponse({"success": False, "error": "login_required"}, status=401)
        product = get_object_or_404(Product, id=id)
        cart_item = Cart.objects.filter(user=request.user, product_id=id).first()
        if cart_item:
            cart_item.delete()
            action = "removed"
        else:
            Cart.objects.create(user=request.user, product_id=id, quantity=1)
            action = "added"
        cart_count = Cart.objects.filter(user=request.user).count()
        return JsonResponse({"success": True, "action": action, "cart_count": cart_count})
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=500)


# ─── AJAX: TOGGLE WISHLIST ───────────────────────────────────────────────────
@require_POST
def toggle_wishlist_ajax(request, id):
    try:
        if not request.user.is_authenticated:
            return JsonResponse({"success": False, "error": "login_required"}, status=401)
        product = get_object_or_404(Product, id=id)
        wish_item = Wishlist.objects.filter(user=request.user, product_id=id).first()
        if wish_item:
            wish_item.delete()
            action = "removed"
        else:
            Wishlist.objects.create(
                user=request.user,
                product_id=id,
                product_name=product.Product_Name,
                product_price=product.Unit_Price,
                product_image=product.ProductImage if product.ProductImage else "",
            )
            action = "added"
        wish_count = Wishlist.objects.filter(user=request.user).count()
        return JsonResponse({"success": True, "action": action, "wishlist_count": wish_count})
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=500)


# ─── CART PAGE ───────────────────────────────────────────────────────────────
@login_required
def cart(request):
    cart_items = Cart.objects.filter(user=request.user)
    # Attach product info from adminpanel_product
    items_with_product = []
    total_price = 0
    for item in cart_items:
        try:
            product = Product.objects.get(id=item.product_id)
            item.product = product
            items_with_product.append(item)
            total_price += float(product.Unit_Price) * item.quantity
        except Product.DoesNotExist:
            pass
    return render(request, "cart.html", {
        "cart_items": items_with_product,
        "total_price": round(total_price, 2),
    })


@login_required
def add_to_cart(request, id):
    product = get_object_or_404(Product, id=id)
    cart_item = Cart.objects.filter(user=request.user, product_id=id).first()
    if cart_item:
        cart_item.quantity += 1
        cart_item.save()
    else:
        Cart.objects.create(user=request.user, product_id=id, quantity=1)
    return redirect("cart")


@login_required
@require_POST
def update_cart(request, item_id):
    try:
        cart_item = get_object_or_404(Cart, id=item_id, user=request.user)
        data = json.loads(request.body)
        quantity = int(data.get("quantity", 1))
        if quantity >= 1:
            cart_item.quantity = quantity
            cart_item.save()
        # Recalculate total
        cart_items = Cart.objects.filter(user=request.user)
        total_price = 0
        for ci in cart_items:
            try:
                p = Product.objects.get(id=ci.product_id)
                total_price += float(p.Unit_Price) * ci.quantity
            except Product.DoesNotExist:
                pass
        return JsonResponse({"success": True, "total_price": round(total_price, 2)})
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)})


@login_required
@require_POST
def remove_cart(request, item_id):
    try:
        cart_item = get_object_or_404(Cart, id=item_id, user=request.user)
        cart_item.delete()
        cart_items = Cart.objects.filter(user=request.user)
        total_price = 0
        for ci in cart_items:
            try:
                p = Product.objects.get(id=ci.product_id)
                total_price += float(p.Unit_Price) * ci.quantity
            except Product.DoesNotExist:
                pass
        return JsonResponse({
            "success": True,
            "total_price": round(total_price, 2),
            "item_count": cart_items.count()
        })
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)})


# ─── WISHLIST PAGE ───────────────────────────────────────────────────────────
@login_required
def wishlist_view(request):
    wishlist_items = Wishlist.objects.filter(user=request.user)
    items_with_product = []
    for item in wishlist_items:
        try:
            product = Product.objects.get(id=item.product_id)
            item.product = product
        except Product.DoesNotExist:
            item.product = None
        items_with_product.append(item)
    return render(request, "wishlist.html", {"wishlist_items": items_with_product})


# ─── ORDER ───────────────────────────────────────────────────────────────────
@login_required
def order_form(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, "order_form.html", {"product": product})


@login_required
@require_POST
def place_order(request):
    product_id = request.POST.get("product_id")
    if product_id:
        product = get_object_or_404(Product, id=product_id)
        quantity = int(request.POST.get("quantity", 1))
        order = Order.objects.create(
            user=request.user,
            full_name=request.POST.get("full_name", ""),
            email=request.POST.get("email", request.user.email),
            phone=request.POST.get("phone", ""),
            address=request.POST.get("address", ""),
            city=request.POST.get("city", ""),
            pincode=request.POST.get("pincode", ""),
            payment_mode=request.POST.get("payment_mode", "COD"),
            total_amount=float(product.Unit_Price) * quantity,
        )
        OrderItem.objects.create(
            order=order,
            product_id=product.id,
            quantity=quantity,
            price=float(product.Unit_Price)
        )
        return render(request, "order_success.html", {"order": order})

    # Cart checkout
    cart_items = Cart.objects.filter(user=request.user)
    if not cart_items.exists():
        return redirect("cart")
    total_amount = 0
    order = Order.objects.create(
        user=request.user,
        full_name=request.POST.get("full_name", ""),
        email=request.POST.get("email", request.user.email),
        phone=request.POST.get("phone", ""),
        address=request.POST.get("address", ""),
        city=request.POST.get("city", ""),
        pincode=request.POST.get("pincode", ""),
        payment_mode=request.POST.get("payment_mode", "COD"),
        total_amount=0,
    )
    for item in cart_items:
        try:
            p = Product.objects.get(id=item.product_id)
            total_amount += float(p.Unit_Price) * item.quantity
            OrderItem.objects.create(
                order=order,
                product_id=p.id,
                quantity=item.quantity,
                price=float(p.Unit_Price)
            )
        except Product.DoesNotExist:
            pass
    order.total_amount = total_amount
    order.save()
    cart_items.delete()
    return render(request, "order_success.html", {"order": order})


@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    
    # We also need to fetch wishlist/cart counts for the header to render correctly
    wishlist_product_ids = Wishlist.objects.filter(user=request.user).values_list('product_id', flat=True) if request.user.is_authenticated else []
    cart_product_ids = Cart.objects.filter(user=request.user).values_list('product_id', flat=True) if request.user.is_authenticated else []

    context = {
        'orders': orders,
        'wishlist_product_ids': wishlist_product_ids,
        'cart_product_ids': cart_product_ids,
    }
    return render(request, "my_orders.html", context)