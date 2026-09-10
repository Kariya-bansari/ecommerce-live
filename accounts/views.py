from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages


# ================= HOME =================
def home(request):
    return render(request, "home.html")


# ================= REGISTER =================
def register(request):
    msg = None

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        email    = request.POST.get("email", "").strip()
        password = request.POST.get("password", "")
        confirm  = request.POST.get("confirm_password", "")

        # --- Server-side validation ---
        if password != confirm:
            return render(request, "register.html", {"msg": "Passwords do not match!"})

        if len(password) < 6:
            return render(request, "register.html", {"msg": "Password must be at least 6 characters."})

        if User.objects.filter(username=username).exists():
            return render(request, "register.html", {"msg": "Username already taken. Please choose another."})

        if User.objects.filter(email=email).exists():
            return render(request, "register.html", {"msg": "Email already registered. Please login."})

        # --- Create Django User (hashed password, session-ready) ---
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
        )
        user.save()

        # Auto-login after registration
        login(request, user)
        return render(request, "register.html", {"msg": "Registration Successful! Welcome, " + username + "!"})

    return render(request, "register.html", {"msg": msg})


# ================= LOGIN =================
def login_view(request):
    if request.user.is_authenticated:
        return redirect("home")

    error = None

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")

        # Support login by email too
        if "@" in username:
            try:
                user_obj = User.objects.get(email=username)
                username = user_obj.username
            except User.DoesNotExist:
                error = "No account found with that email."
                return render(request, "login.html", {"error": error})

        # Django's authenticate checks hashed password
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)  # Creates session + sets auth cookies
            # Redirect to next page if provided, else home
            next_url = request.GET.get("next", "home")
            return redirect(next_url)
        else:
            error = "Invalid username or password. Please try again."

    return render(request, "login.html", {"error": error})


# ================= LOGOUT =================
def logout_view(request):
    logout(request)  # Clears Django session + auth cookies
    return redirect("login")


# ================= DASHBOARD (admin only) =================
@login_required
def dashboard(request):
    if not request.user.is_staff:
        return redirect("home")
    return render(request, "admin_dashboard.html")


# ================= ADD PRODUCT =================
@login_required
def api_add_product(request):
    if not request.user.is_staff:
        return JsonResponse({"error": "Unauthorized"}, status=403)

    if request.method == "POST":
        from .models import Product

        product_name = request.POST.get("product_name")
        category     = request.POST.get("category")
        brand        = request.POST.get("brand")
        model_type   = request.POST.get("model_type")
        quantity     = int(request.POST.get("quantity", 0))
        unit_price   = float(request.POST.get("unit_price", 0))
        gst_percent  = float(request.POST.get("gst_percent", 0))
        total        = unit_price + (unit_price * gst_percent / 100)

        image      = request.FILES.get("product_image")
        image_name = image.name if image else ""

        Product.objects.create(
            product_name=product_name,
            category=category,
            brand=brand,
            model_type=model_type,
            quantity=quantity,
            unit_price=unit_price,
            gst_percent=gst_percent,
            total_price=round(total, 2),
            product_image=image_name,
        )
        return JsonResponse({"status": "ok"})

    return JsonResponse({"error": "POST required"}, status=405)


# ================= GET PRODUCTS =================
def api_products(request):
    from .models import Product
    products = list(Product.objects.values())
    return JsonResponse(products, safe=False)


# ================= PLACE ORDER =================
@login_required
def place_order(request):
    from .models import Order

    if request.method == "POST":
        Order.objects.create(
            full_name=request.POST.get("name", ""),
            email=request.POST.get("email", request.user.email),
            product_name=request.POST.get("product", ""),
            quantity=int(request.POST.get("quantity", 1)),
            payment_method=request.POST.get("payment", "COD"),
            shipping_address=request.POST.get("address", ""),
        )
        return redirect("dashboard")

    return render(request, "order_form.html")