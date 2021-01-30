from django.urls import  path
from django.conf import settings
from django.conf.urls.static import static

from . import views
from .views import HomeView, ItemDetailView, add_to_cart, remove_from_cart, OrderSummaryView, \
    remove_item_from_cart, add_item_to_cart, CheckoutView, CategoryView, AboutView

app_name = 'core'

urlpatterns = [
    path('shop/', HomeView.as_view(), name='shop'),
    path('about/', AboutView.as_view(), name='about'),
    path('contact/', views.contact_us, name='contact'),
    path('product/<slug>/', ItemDetailView.as_view(), name='product'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('order-summary/', OrderSummaryView.as_view(), name='order-summary'),
    path('add-to-cart/<slug>', add_to_cart, name='add-to-cart'),
    path('remove-from-cart/<slug>', remove_from_cart, name='remove-from-cart'),
    path('remove_item_from_cart/<slug>', remove_item_from_cart, name='remove_item_from_cart'),
    path('add_item_to_cart/<slug>', add_item_to_cart, name='add_item_to_cart'),
    path('search/', CategoryView.as_view(), name='search'),
    path('', views.landing_page, name='landing'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)