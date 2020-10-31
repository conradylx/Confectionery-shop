from django.db import models
from django.conf import settings
from django.db.models import Model

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
    category = models.CharField(choices=CATEGORY_CHOICE, max_length=1)
    label = models.CharField(choices=LABEL_CHOICE, max_length=1)

    def __str__(self):
        return self.title


class OrderItem(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    order_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return self.username