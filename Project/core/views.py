from django.shortcuts import render

from .models import Item


def products(request):
    context = {
        "items" : Item.objects.all()
    }
    return render(request, 'product.html', context)


def checkout(request):
    return render(request, 'checkout.html')


def home(request):
    context = {
        "items": Item.objects.all()
    }
    return render(request, 'home.html', context)