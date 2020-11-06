from django.db import models
from django.conf import settings
from django.db.models import Model, Sum
from django.urls import reverse


CATEGORY_CHOICE = {
    ('K','Kruche'),
    ('S','Serniki'),
    ('D','Drożdżowe')
}
LABEL_CHOICE = {
    ('P','primary'),
    ('S','secondary'),
    ('D','danger')
}


class Item(models.Model):
    title = models.CharField(max_length=120)
    price = models.FloatField()
    disc_price = models.FloatField(blank=True, null=True)
    category = models.CharField(choices=CATEGORY_CHOICE, max_length=1)
    label = models.CharField(choices=LABEL_CHOICE, max_length=1)
    slug = models.SlugField()
    descr = models.TextField()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("core:product",kwargs={
            'slug': self.slug
        })

    def get_add_to_cart_url(self):
        return reverse("core:add-to-cart", kwargs={
            'slug': self.slug
        })

    def get_remove_from_cart_url(self):
        return reverse("core:remove-from-cart", kwargs={
            'slug': self.slug
        })


class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.item.title}"

    def get_total_price(self):
        return self.quantity * self.item.price

    def get_total_disc_price(self):
        return self.quantity * self.item.disc_price

    def get_amount_save(self):
        return self.get_total_price() - self.get_total_disc_price()

    def get_final_price(self):
        if self.item.disc_price:
            return self.get_total_disc_price()
        else:
            return self.get_total_price()


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered = models.BooleanField(default=False)
    ordered_date = models.DateTimeField()

    def __str__(self):
        return self.user.username

    def get_total(self):
        total = 0
        for order in self.items.all():
            total += order.get_final_price()
        return total