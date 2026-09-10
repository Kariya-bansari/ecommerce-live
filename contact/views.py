from django.shortcuts import render
from .models import ContactMessage

def contact(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        ContactMessage.objects.create(
            name=name,
            email=email,
            subject=subject,
            message=message
        )

        return render(request, "contact.html", {"success": "Message Sent Successfully!"})

    return render(request, "contact.html")