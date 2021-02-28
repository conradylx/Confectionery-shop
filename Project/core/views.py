from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.views import View
from django.views.generic import ListView, DetailView
from django.db.models import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist

from .forms import CheckOutForm, ContactForm
from .models import Item, Order, OrderItem, BillingAddress, Category


class CheckoutView(View):
    def get(self, *args, **kwargs):
        form = CheckOutForm()
        order = Order.objects.get(user=self.request.user, ordered=False)
        context = {
            'form': form,
            'ordered_items': order,
        }
        return render(self.request, 'checkout.html', context)

    def post(self, *args, **kwargs):
        form = CheckOutForm(self.request.POST or None, initial={'country': 'PL'})
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            if form.is_valid():
                street_address = form.cleaned_data.get('street_address')
                apartment_address = form.cleaned_data.get('apartment_address')
                country = form.cleaned_data.get('country')
                city = form.cleaned_data.get('city')
                zip = form.cleaned_data.get('zip')
                billing_address = BillingAddress(
                    user=self.request.user,
                    street_address=street_address,
                    apartment_address=apartment_address,
                    country=country,
                    city=city,
                    zip=zip
                )
                billing_address.save()
                order.billing_address = billing_address
                order.ordered = True
                order.save()
                messages.info(self.request, "Dziękujemy za zakupy w naszym sklepie!")
                return redirect('core:shop')
            messages.warning(self.request, "Failed check out")
            return redirect('core:checkout')
        except ObjectDoesNotExist:
            messages.error(request="Dziękujemy za zakupy w naszym sklepie!")
            return redirect("core:shop")


class HomeView(ListView):
    model = Item
    paginate_by = 8
    template_name = "home.html"
    context_object_name = "cakes"

    def get_queryset(self, *args, **kwargs):
        category_id = self.request.GET.get('category')
        if category_id:
            items = Item.get_products_by_category(category_id)
        else:
            items = Item.get_all_products()
        return items

    def get_context_data(self, *args, **kwargs):
        category_menu = Category.objects.all()
        context_items = super(HomeView, self).get_context_data(*args, **kwargs)
        context_items["category_menu"] = category_menu
        return context_items


class AboutView(ListView):
    model = Item
    template_name = "about.html"


class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object': order
            }
            return render(self.request, 'order-summary.html', context)
        except ObjectDoesNotExist:
            # messages.error(request="You dont have active orders")
            messages.error(request="Koszyk jest pusty.")
            return redirect("/")


class ItemDetailView(DetailView):
    model = Item
    template_name = "product.html"
    context_object_name = "product"

    def get_context_data(self, **kwargs):
        context = super(ItemDetailView, self).get_context_data(**kwargs)
        # context2 = super(ItemDetailView, self).get_context_data(**kwargs)
        context_related = Category.objects.filter(id__in=self.object.get_products_by_category(self.object.category.id))
        context_related2 = Item.objects.filter(category__in=context_related)[:3]
        context['related'] = context_related2
        print(context_related2)
        return context

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
            messages.info(request, "Koszyk został zaktualizowany.")
            return redirect("core:order-summary")
        else:
            messages.info(request, "Produkt został dodany do koszyka.")
            order.items.add(order_item)
            return redirect("core:order-summary")
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "Produkt został zaktualizowany w koszyku.")

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
            messages.info(request, "Produkt został usunięty z koszyka.")
            return redirect("core:order-summary")
        else:
            messages.info(request, "Produkt nie znajduje się w koszyku.")
            return redirect("core:product", slug=slug)
    else:
        messages.info(request, "Brak aktywnego zamówienia")
        return redirect("core:product", slug=slug)

@login_required
def remove_from_order(request):
    item = get_object_or_404(Item)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(Q(item__slug=item.slug)).exists():
            order_item = OrderItem.objects.filter(
                item=item, user=request.user, ordered=False
            )[0]
            order.items.remove(order_item)
            order_item.delete()
            return redirect("core:order-summary")

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
            messages.info(request, "Zaktualizowano ilość produktu.")
            return redirect("core:order-summary")
        else:
            messages.info(request, "Produkt nie znajduje się w koszyku.")
            return redirect("core:product", slug=slug)
    else:
        messages.info(request, "Brak zamówień.")
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
            messages.info(request, "Zaktualizowano ilość produktu.")
            return redirect("core:order-summary")
        else:
            messages.info(request, "Produkt nie znajduje się w koszyku.")
            return redirect("core:product", slug=slug)
    else:
        messages.info(request, "Brak zamówień.")
        return redirect("core:product", slug=slug)


class CategoryView(ListView):
    model = Item
    template_name = "search.html"
    context_object_name = "all_search_results"

    def get_queryset(self):
        result = super(CategoryView, self).get_queryset()
        query = self.request.GET.get('search')
        if query:
            object_list = Item.objects.filter(title__icontains=query)
            result = object_list
        else:
            result = None
        return result

    def get_context_data(self, *args, **kwargs):
        category_id = self.request.GET.get('category')
        category_menu = Category.objects.all()
        if category_id:
            items = Item.get_products_by_category(category_id)
        else:
            items = Item.get_all_products()
        context_items = super(CategoryView, self).get_context_data(*args, **kwargs)
        context_items["category_list"] = items
        context_items["category_menu"] = category_menu
        return context_items


def contact_us(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            sender_name = form.cleaned_data['name']
            sender_email = form.cleaned_data['email']
            message = "{0} wyslal wiadomosc:\n\n{1}".format(sender_name, form.cleaned_data['message'])
            send_mail('New Enquiry', message, sender_email, ['frankysanky@gmail.com'])
            return HttpResponse('Dziękujemy za kontakt! Odezwiemy się tak szybko jak to możliwe.')
    else:
        form = ContactForm()
    context = {
        "form": form
    }
    return render(request, 'contact.html', context)


def landing_page(request):
    return render(request, 'landing.html')
