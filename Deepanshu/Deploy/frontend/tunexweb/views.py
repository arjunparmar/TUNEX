from django.shortcuts import render


def tunex_home(request, *args, **kwargs):
    return render(request, "index.html")


def staticpage(request, *args, **kwargs):
    return render(request, "static.html")


def aboutpage(request, *args, **kwargs):
    return render(request, "about.html")


def uploadImage(request, *args, **kwargs):
    pic = request.FILES['staticimage']

    from .models import User
    user = User(img=pic)
    user.save()
    return render(request, "static.html")
