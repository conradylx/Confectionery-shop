from django.urls import  path

from . import views
from .views import HomeView, ItemDetailView, add_to_cart, remove_from_cart, OrderSummaryView, \
    remove_item_from_cart, add_item_to_cart, CheckoutView, SearchView

app_name = 'core'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('product/<slug>/', ItemDetailView.as_view(), name='product'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('order-summary/', OrderSummaryView.as_view(), name='order-summary'),
    path('add-to-cart/<slug>', add_to_cart, name='add-to-cart'),
    path('remove-from-cart/<slug>', remove_from_cart, name='remove-from-cart'),
    path('remove_item_from_cart/<slug>', remove_item_from_cart, name='remove_item_from_cart'),
    path('add_item_to_cart/<slug>', add_item_to_cart, name='add_item_to_cart'),
    path('search/', SearchView.as_view(), name='search'),
]