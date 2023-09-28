import stripe
from django.conf import settings
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models


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


