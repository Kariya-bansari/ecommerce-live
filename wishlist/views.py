from django.shortcuts import render, redirect
from .models import Wishlist

def wishlist_page(request):
    products = Wishlist.objects.all()   # ✅ change variable name
    return render(request, 'wishlist.html', {'products': products})

def add_wishlist(request):
    if request.method == "POST":
        Wishlist.objects.create(
            product_name=request.POST.get('product_name'),
            product_price=request.POST.get('product_price'),
            product_image=request.FILES.get('product_image')
        )
        return redirect('wishlist')