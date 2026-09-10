from django.shortcuts import render, redirect
from .models import Gallery

# Public Gallery Page (for navbar)
def gallery(request):
    galleries = Gallery.objects.all().order_by('-uploaded_at')
    return render(request, 'gallery.html', {'galleries': galleries})


# Admin Upload Page
def admin_add_gallery(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        image = request.FILES.get('image')

        if title and image:
            Gallery.objects.create(
                title=title,
                description=description,
                image=image
            )
            return redirect('admin_add_gallery')

    galleries = Gallery.objects.all().order_by('-uploaded_at')
    return render(request, 'admin_add_gallery.html', {'galleries': galleries})