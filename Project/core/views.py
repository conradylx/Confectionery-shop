from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.views.generic import ListView, DetailView
from django.db.models import *
from django.contrib import messages
from .models import Item, Order, OrderItem


def products(request):
    context = {
        "items": Item.objects.all()
    }
    return render(request, 'product.html', context)


def checkout(request):
    return render(request, 'checkout.html')


class HomeView(ListView):
    model = Item
    template_name = "home.html"


class ItemDetailView(DetailView):
    model = Item
    template_name = "product.html"


def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )
    order = Order.objects.filter(user=request.user, ordered=False)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(Q(item__slug=item.slug)).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "This item was successfully updated to your cart")
        else:
            messages.info(request, "This item was successfully added to your cart")
            order.items.add(order_item)
            return redirect("core:product", slug=slug)
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "This item was successfully updated to your cart")

    return redirect("core:product", slug=slug)


def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(Q(item__slug=item.slug)).exists():
            order_item = OrderItem.objects.filter(
                item=item, user=request.user, ordered=False
            )[0]
            order.items.remove(order_item)
            order.item.delete()
            messages.info(request, "This item was removed from your cart.")
            return redirect("core:product", slug=slug)
        else:
            messages.info(request, "This item is not in your cart")
            return redirect("core:product", slug=slug)
    else:
        messages.info(request, "You dont have an order ")
        return redirect("core:product", slug=slug)