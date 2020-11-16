from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.views import View
from django.views.generic import ListView, DetailView
from django.db.models import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist

from .forms import CheckOutForm
from .models import Item, Order, OrderItem, BillingAddress, Category


def products(request):
    context = {
        "items": Item.objects.all()
    }
    return render(request, 'categories.html', context)


class CheckoutView(View):
    def get(self, *args, **kwargs):
        form = CheckOutForm()
        context = {
            'form': form
        }
        return render(self.request, 'checkout.html', context)

    def post(self, *args, **kwargs):
        form = CheckOutForm(self.request.POST or None)
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            if form.is_valid():
                street_address = form.cleaned_data.get('street_address')
                apartment_address = form.cleaned_data.get('apartment_address')
                country = form.cleaned_data.get('country')
                zip = form.cleaned_data.get('zip')
                # same_billing_address = form.cleaned_data.get('same_billing_address')
                # save_info = form.cleaned_data.get('save_info')
                payment_option = form.cleaned_data.get('payment_option')
                billing_address = BillingAddress(
                    user=self.request.user,
                    street_address=street_address,
                    apartment_address=apartment_address,
                    country=country,
                    zip=zip
                )
                billing_address.save()
                order.billing_address = billing_address
                order.save()
                return redirect('core:checkout')
            messages.warning(self.request, "Failed check out")
            return redirect('core:checkout')
        except ObjectDoesNotExist:
            messages.error(request="You dont have active orders")
            return redirect("core:order_summary")


class HomeView(ListView):
    model = Item
    paginate_by = 4
    template_name = "home.html"

    def get_context_data(self, *args, **kwargs):
        category_menu = Category.objects.all()
        context_items = super(HomeView, self).get_context_data(*args, **kwargs)
        context_items["category_menu"] = category_menu
        return context_items

    def get_context_data(self, *args, **kwargs):
        category_id = self.request.GET.get('category')
        category_menu = Category.objects.all()
        if category_id:
            items = Item.get_products_by_category(category_id)
            print(items)
        else:
            items = Item.get_all_products()
        context_items = super(HomeView, self).get_context_data(*args, **kwargs)
        context_items["category_list"] = items
        context_items["category_menu"] = category_menu
        return context_items


class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object': order
            }
            return render(self.request, 'order-summary.html', context)
        except ObjectDoesNotExist:
            messages.error(request="You dont have active orders")
            return redirect("/")


class ItemDetailView(DetailView):
    model = Item
    template_name = "product.html"


@login_required
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
            return redirect("core:order-summary")
        else:
            messages.info(request, "This item was successfully added to your cart")
            order.items.add(order_item)
            return redirect("core:order-summary")
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "This item was successfully updated to your cart")

    return redirect("core:order-summary")


@login_required
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
            order_item.delete()
            messages.info(request, "This item was removed from your cart.")
            return redirect("core:order-summary")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("core:product", slug=slug)
    else:
        messages.info(request, "You do not have an active order")
        return redirect("core:product", slug=slug)


@login_required
def remove_item_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(Q(item__slug=item.slug)).exists():
            order_item = OrderItem.objects.filter(
                item=item, user=request.user, ordered=False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
            messages.info(request, "This item quantity was updated")
            return redirect("core:order-summary")
        else:
            messages.info(request, "This item is not in your cart")
            return redirect("core:product", slug=slug)
    else:
        messages.info(request, "You dont have an order ")
        return redirect("core:product", slug=slug)


@login_required
def add_item_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(Q(item__slug=item.slug)).exists():
            order_item = OrderItem.objects.filter(
                item=item, user=request.user, ordered=False
            )[0]
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "This item quantity was updated")
            return redirect("core:order-summary")
        else:
            messages.info(request, "This item is not in your cart")
            return redirect("core:product", slug=slug)
    else:
        messages.info(request, "You dont have an order ")
        return redirect("core:product", slug=slug)
