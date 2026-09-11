from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.contrib import messages
from django.db.models import Sum, Count
from .models import Product
from store.models import Order, OrderItem, Cart, Wishlist
from django.contrib.auth.models import User
import json


def home(request):
    return render(request, "home.html")


def dashboard(request):
    products = Product.objects.all()
    total_products = products.count()
    total_stock = sum(p.Quantity for p in products)
    total_revenue = sum((p.Total_Price or 0) * p.Quantity for p in products)
    low_stock = products.filter(Quantity__lte=5)

    # ── CHART 1: Category Share (Donut) ──────────────────
    # Group products by category, count items per category
    category_data = (
        products.values('Category')
        .annotate(count=Count('id'))
        .order_by('-count')
    )
    cat_labels = [item['Category'] or 'Uncategorized' for item in category_data]
    cat_counts = [item['count'] for item in category_data]

    # ── CHART 2: Top 8 Products by Total Price (Bar) ──────
    top_products = products.order_by('-Total_Price')[:8]
    bar_labels = [p.Product_Name[:20] for p in top_products]   # trim long names
    bar_prices = [float(p.Total_Price or 0) for p in top_products]

    return render(request, "admin_dashboard.html", {
        "products": products,
        "total_products": total_products,
        "total_stock": total_stock,
        "total_revenue": total_revenue,
        "low_stock": low_stock,
        "low_stock_count": low_stock.count(),
        # Chart data — passed as JSON strings so JS can parse safely
        "cat_labels": json.dumps(cat_labels),
        "cat_counts": json.dumps(cat_counts),
        "bar_labels": json.dumps(bar_labels),
        "bar_prices": json.dumps(bar_prices),
        # Live data from user orders
        "all_orders": Order.objects.all().order_by('-created_at'),
        "all_users": User.objects.filter(is_staff=False).order_by('-date_joined'),
        "cart_items": Cart.objects.all().select_related('user'),
        "wishlist_items": Wishlist.objects.all().select_related('user'),
        "total_orders": Order.objects.count(),
        "total_users": User.objects.filter(is_staff=False).count(),
    })


def api_products(request):
    products = Product.objects.all()
    data = []
    for p in products:
        data.append({
            "id": p.id,
            "Product_Name": p.Product_Name,
            "Category": p.Category,
            "Brand": p.Brand,
            "Model_Type": p.Model_Type,
            "Quantity": p.Quantity,
            "Unit_Price": str(p.Unit_Price),
            "Gst_Percent": str(p.Gst_Percent) if p.Gst_Percent else "0",
            "Total_Price": str(p.Total_Price) if p.Total_Price else "0",
            "ProductImage": p.ProductImage.url if p.ProductImage else "",
        })
    return JsonResponse(data, safe=False)


def add_product(request):
    if request.method == "POST":
        try:
            unit_price = float(request.POST.get('Unit_Price', 0))
            gst = float(request.POST.get('Gst_Percent', 0) or 0)
            total = round(unit_price + (unit_price * gst / 100), 2)
            Product.objects.create(
                Product_Name=request.POST.get('Product_Name'),
                Category=request.POST.get('Category'),
                Brand=request.POST.get('Brand'),
                Model_Type=request.POST.get('Model_Type'),
                Quantity=int(request.POST.get('Quantity', 0)),
                Unit_Price=unit_price,
                Gst_Percent=gst,
                Total_Price=total,
                ProductImage=request.FILES.get('ProductImage'),
            )
            messages.success(request, "Product added successfully!")
            return redirect('dashboard')
        except Exception as e:
            messages.error(request, f"Error adding product: {e}")
    return render(request, "admin_add_product.html")


def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        try:
            product.Product_Name = request.POST.get('Product_Name')
            product.Category = request.POST.get('Category')
            product.Brand = request.POST.get('Brand')
            product.Model_Type = request.POST.get('Model_Type')
            product.Quantity = int(request.POST.get('Quantity', 0))
            unit_price = float(request.POST.get('Unit_Price', 0))
            gst = float(request.POST.get('Gst_Percent', 0) or 0)
            product.Unit_Price = unit_price
            product.Gst_Percent = gst
            product.Total_Price = round(unit_price + (unit_price * gst / 100), 2)
            if request.FILES.get('ProductImage'):
                product.ProductImage = request.FILES.get('ProductImage')
            product.save()
            messages.success(request, "Product updated successfully!")
            return redirect('dashboard')
        except Exception as e:
            messages.error(request, f"Error updating product: {e}")
    return render(request, "admin_edit_product.html", {"product": product})


def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        product.delete()
        messages.success(request, f'"{product.Product_Name}" deleted successfully.')
        return redirect('dashboard')
    return render(request, "admin_confirm_delete.html", {"product": product})


def product_list(request):
    products = Product.objects.all()
    return render(request, "product_list.html", {"products": products})


def add_to_cart(request, id):
    return HttpResponse(f"Product {id} added to cart")


def cart_view(request):
    return render(request, "cart.html")


def add_to_wishlist(request, id):
    return HttpResponse("Added to wishlist")


def delivery(request):
    return render(request, "delivery.html")