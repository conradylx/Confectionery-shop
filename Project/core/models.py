from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.conf import settings
from django.db.models import Model, Sum
from django.urls import reverse
from django_countries.fields import CountryField

LABEL_CHOICE = {
    ('P', 'primary'),
    ('S', 'secondary'),
    ('D', 'danger')
}


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Kategorie"
        verbose_name_plural = "Kategorie"

    def get_absolute_url(self):
        return reverse('home')

    @staticmethod
    def get_all_categories(self):
        return Category.objects.all()


class Item(models.Model):
    title = models.CharField(max_length=120)
    price = models.FloatField()
    disc_price = models.FloatField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    label = models.CharField(choices=LABEL_CHOICE, max_length=1, null=True)
    slug = models.SlugField()
    descr = models.TextField()
    image = models.ImageField(upload_to="static_files_proj/img/products/")
    weight = models.CharField(default=100, max_length=15)
    calories = models.PositiveIntegerField(default=0, validators=[MinValueValidator(1), MaxValueValidator(100)])
    allergens = models.CharField(default="brak", max_length=30)

    class Meta:
        verbose_name = ("Ciasto")
        verbose_name_plural = ("Ciasta")

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

    @staticmethod
    def get_all_products():
        return Item.objects.all()

    @staticmethod
    def get_products_by_category(category_id):
        if category_id:
            return Item.objects.filter(category = category_id)
        else:
            return Item.get_all_products()


class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    class Meta:
        verbose_name = ("Zamówione ciasta")
        verbose_name_plural = ("Zamówione ciasta")

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

    def get_order_items(self):
        return self.quantity


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered = models.BooleanField(default=False)
    ordered_date = models.DateTimeField(auto_now=True)
    billing_address = models.ForeignKey('BillingAddress', on_delete=models.SET_NULL,blank=True,null=True)

    class Meta:
        verbose_name = "Zamówienia"
        verbose_name_plural = "Zamówienia"

    def __str__(self):
        return self.user.username

    def get_total(self):
        total = 0
        for order in self.items.all():
            total += order.get_final_price()
        return total

    def get_total_items(self):
        total = 0
        for order in self.items.all():
            total += order.get_order_items()
        return total


class BillingAddress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    street_address = models.CharField(max_length=200)
    apartment_address = models.CharField(max_length=200)
    country = CountryField(multiple=False)
    city = models.CharField(max_length=120)
    zip = models.CharField(max_length=200)

    def __str__(self):
        return self.user.username

    class Meta():
        verbose_name = "Dane kontaktowe"
        verbose_name_plural = "Dane kontaktowe"