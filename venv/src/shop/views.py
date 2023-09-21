import stripe
from django.conf import settings
from django.forms import modelformset_factory
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView

from accounts.models import Shopper, ShippingAddress
from shop.forms import OrderForm
from shop.models import Cart, Shop, Order

stripe.api_key = settings.STRIPE_API_KEY
endpoint_secret = settings.ENDPOINT_SECRET

# Create your views here.


class BooksListView(ListView):
    model = Shop
    context_object_name = 'books'
    template_name = 'shop/books_list.html'

class BooksDetailView(DetailView):
    model = Shop
    context_object_name = 'book'
    template_name = 'shop/books_detail.html'

def cart(request):
    OrderFormSet = modelformset_factory(Order, form=OrderForm, extra=0)
    formset = OrderFormSet(queryset=Order.objects.filter(user=request.user))
    return render(request, 'shop/cart.html', context={"forms": formset})

def add_to_cart(request, slug):
    user = request.user
    shop = get_object_or_404(Shop, slug=slug)
    cart, _ = Cart.objects.get_or_create(user=user)
    order, created = Order.objects.get_or_create(user=user, ordered=False, shop=shop)
    if created:
        cart.orders.add(order)
        cart.save()
    else:
        order.quantity += 1
        order.save()

    return redirect('../..')

def checkout_success(request):
    user = request.user
    cart = Cart.objects.filter(user)
    cart.delete()
    return render(request, 'shop/checkout_success.html')

def complete_order(data, user):
    user.stripe_id = data['customer']
    user.cart.delete()
    user.save()
    return HttpResponse(status=200)

def create_checkout_session(request):
    cart = request.user.cart
    line_items = [{"price": order.shop.strip_id,
                 "quantity": order.quantity}for order in cart.orders.all()]

    checkout_data = {
        "locale":"fr",
        "payment_method_types":['card'],
        "line_items":line_items,
        "mode":'payment',
        "shipping_address_collection":{"allowed_countries":["FR"]},
        "success_url":request.build_absolute_uri(reverse('shop:checkout_success')),
        "cancel_url":'http://127.0.0.1:8000/',
    }

    if request.user.stripe_id:
        checkout_data["customer"] = request.user.stripe_id
    else:
        checkout_data["customer_email"] = request.user.email

    checkout_session = stripe.checkout.Session.create(**checkout_data)

    return redirect(checkout_session.url, status=303)

@csrf_exempt
def my_webhook_view(request):
  payload = request.body
  sig_header = request.META['HTTP_STRIPE_SIGNATURE']
  event = None

  try:
    event = stripe.Webhook.construct_event(
      payload, sig_header, endpoint_secret
    )
  except ValueError as e:
    # Invalid payload
    return HttpResponse(status=400)
  except stripe.error.SignatureVerificationError as e:
    # Invalid signature
    return HttpResponse(status=400)

  if event['type'] == "checkout.session.completed":
      data = event['data']['object']
      try:
          user = get_object_or_404(Shopper, email=data['customer_details']['email'])
      except KeyError:
          return HttpResponse("Invalid user email", status=404)

      complete_order(data=data, user=user)
      save_shipping_address(data=data, user=user)
      return  HttpResponse(status=200)

  return HttpResponse(status=200)

def save_shipping_address(data, user):
    try:
        address = data["shipping"]["address"]
        name = data["shipping"]["name"]
        city = address["city"]
        country = address["country"]
        line1 = address["line1"]
        line2 = address["line2"]
        zip_code = address["postal_code"]
    except KeyError:
        return HttpResponse(status=400)

    ShippingAddress.objects.get_or_create(user=user,
                                          name=name,
                                          city=city,
                                          country=country.lower(),
                                          address_1=line1,
                                          address_2=line2 or "",
                                          zip_code=zip_code)

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    print(payload)

    return HttpResponse(status=200)


def update_quantities(request):
    OrderFormSet = modelformset_factory(Order, form=OrderForm, extra=0)
    formset = OrderFormSet(request.POST, queryset=Order.objects.filter(user=request.user))
    if formset.is_valid():
        formset.save()
    return redirect("..")