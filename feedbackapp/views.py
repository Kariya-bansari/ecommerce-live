from django.shortcuts import render, redirect
from .models import Feedback

def feedback_view(request):
    if request.method == "POST":
        Feedback.objects.create(
            name=request.POST.get("name"),
            email=request.POST.get("email"),
            message=request.POST.get("message")
        )
        return redirect("feedback")

    feedbacks = Feedback.objects.all()
    return render(request, "feedback.html", {"feedbacks": feedbacks})
