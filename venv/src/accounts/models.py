import stripe
from django.conf import settings
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from iso3166 import countries

# Create your models here.
stripe.api_key = settings.STRIPE_API_KEY

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **kwargs):
        if not email:
            raise ValueError("L'adresse mail est obligatoire")
        email = self.normalize_email(email)
        user = self.model(email=email) # model de la classe Shopper
        user.set_password(password) #encrypter le mot de passe
        user.save()
        return user

    def create_superuser(self, email, password, **kwargs):
        user = self.create_user(email=email, password=password, **kwargs)
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save()
        return user

class Shopper(AbstractUser):
    username = None
    email = models.EmailField(max_length=255, unique=True)
    stripe_id = models.CharField(max_length=100, blank=True)
    forget_password_token = models.CharField(max_length=100, blank=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

ADDRESS_FORMAT = """
{name}
{address_1}
{address_2}
{city}, {zip_code}
{country}
"""

class ShippingAddress(models.Model):
    user:Shopper = models.ForeignKey(Shopper, on_delete=models.CASCADE, related_name="addresses")
    name = models.CharField(max_length=255)
    address_1 = models.CharField(max_length=1500, help_text="Adresse de voirie et numéro de rue")
    address_2 = models.CharField(max_length=1500, help_text="Bâtiment, étage, lieu-dit", blank=True)
    city = models.CharField(max_length=1500)
    zip_code = models.CharField(max_length=50)
    country = models.CharField(max_length=2, choices=[(c.alpha2.lower(), c.name)for c in countries])
    default = models.BooleanField(default=False)

    def __str__(self):
        data = self.__dict__.copy()
        data.update(country=self.get_country_display().upper())
        return ADDRESS_FORMAT.format(**data).strip("\n")

    def as_dict(self):
        return {
            "city": self.city,
            "country": self.country,
            "line1": self.address_1,
            "line2": self.address_2,
            "postal_code": self.zip_code,
        }

    def set_default(self):
        if not self.user.stripe_id:
            raise ValueError(f"User {self.user.email} doesn't have a stripe Customer ID")

        self.user.addresses.update(default=False)
        self.default = True
        self.save()

        stripe.Customer.modify(
            self.user.stripe_id,
            shipping={"name":self.name,
                      "address": {}},
            address=self.as_dict()
        )
