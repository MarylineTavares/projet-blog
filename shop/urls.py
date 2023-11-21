from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from shop.views import BooksListView, BooksDetailView, cart, add_to_cart, create_checkout_session, \
    checkout_success, stripe_webhook, update_quantities

app_name = "shop"

urlpatterns = [
    path('shop/', BooksListView.as_view(), name='books_list'),
    path('shop/<str:slug>/', BooksDetailView.as_view(), name='books_detail'),
    path('shop/<str:slug>/add-to-cart/', add_to_cart, name='add_to_cart'),
    path('cart/', cart, name='cart'),
    path('cart/update-quantities/', update_quantities, name='update_quantities'),
    path('cart/create-checkout-session', create_checkout_session, name='create_checkout_session'),
    path('cart/success', checkout_success, name='checkout_success'),
    path('stripe-webhook/', stripe_webhook, name='stripe_webhook'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
