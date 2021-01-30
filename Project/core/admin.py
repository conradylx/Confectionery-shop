from django.contrib import admin
from django.utils.html import format_html

from .models import Item, OrderItem, Order, Category, BillingAddress


def short_description(self):
    return self.descr if len(self.descr) < 125 else (self.descr[:123] + '..')


class ItemAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ('title', 'price', 'disc_price', 'category', 'label', 'slug', short_description,
                    'weight', 'calories', 'allergens', 'image_tag')
    list_display_links = ['title']
    readonly_fields = ['image_tag']

    def image_tag(self, obj):
        return format_html('<img src="{0}" style="width: 255px; height:155px;" />'.format(obj.image.url))

    image_tag.short_description = "image"
    image_tag.allow_tags = True


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('user', 'item', 'quantity')
    readonly_fields = ['user', 'item', 'quantity']


class OrderAdmin(admin.ModelAdmin):
    model = Order
    list_display = ('user', 'start_date', 'ordered', 'ordered_date', 'billing_address')


class BillingAddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'street_address', 'apartment_address', 'country', 'city', 'zip')


admin.site.register(Item, ItemAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Category)
admin.site.register(BillingAddress, BillingAddressAdmin)

admin.site.site_header = "Shop's administration panel"
admin.site.site_title = "Site admin"
admin.site.index_title = "Administration"
