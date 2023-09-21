from django.db import models
from django.template.defaultfilters import slugify
from django.utils import timezone

from blog.settings import AUTH_USER_MODEL

# Create your models here.
class Shop(models.Model):
    title = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=130, blank=True)
    price = models.FloatField(default=0.0)
    description = models.TextField(blank=True)
    thumbnail = models.ImageField(upload_to='shop', blank=True, null=True)
    strip_id = models.CharField(max_length=90, blank=True)

    def __str__(self):
        return self.title


    def save(self, *args, **kwargs):
        self.slug = self.slug or slugify(self.title)
        return super().save(*args, **kwargs)

class Order(models.Model):
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    ordered = models.BooleanField(default=False)
    ordered_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.shop.name} ({self.quantity})"


class Cart(models.Model):
    user = models.OneToOneField(AUTH_USER_MODEL, on_delete=models.CASCADE)
    orders = models.ManyToManyField(Order)

    def __str__(self):
        return self.user.username

    def delete(self, *args, **kwargs):
        for order in self.orders.all():
            order.ordered = True
            order.ordered_date = timezone.now()
            order.save()
        self.orders.clear()
        super().delete(*args, **kwargs)
