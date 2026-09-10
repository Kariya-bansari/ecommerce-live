from django.shortcuts import render
from .models import Register

def register(request):
    msg = ""

    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        Register.objects.create(
            username=username,
            email=email,
            password=password
        )

        msg = "Registration successful!"

    return render(request, "register.html", {"msg": msg})


def login_view(request):  # Fixed! Added request
    return render(request, 'login.html')