from django.contrib import messages
from django.contrib.auth import get_user_model, login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.forms import model_to_dict
from django.shortcuts import render, redirect, get_object_or_404

from accounts.forms import UserForm
from accounts.models import ShippingAddress

# Create your views here.
User = get_user_model()

def account(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(email=email, password=password)
        if user:
            login(request, user)
            return redirect('../shop/')
    return render(request, 'accounts/account.html')

def create_account(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = User.objects.create_user(email=email, password=password)
        login(request, user)
        return redirect('../..')
    return render(request, 'accounts/create_account.html')

def logout_user(request):
    logout(request)
    return redirect('../..')


@login_required
def profile(request):
    if request.method == "POST":
        is_valid = authenticate(email=request.POST.get("email"), password=request.POST.get("password"))
        if is_valid:
            user = request.user
            user.first_name = request.POST.get('first_name')
            user.last_name = request.POST.get('last_name')
            user.save()
        else:
            messages.add_message(request, messages.ERROR, "Mot de passe invalide")
        return redirect("accounts/profile")
    form = UserForm(initial=model_to_dict(request.user, exclude="password"))
    addresses = request.user.addresses.all()
    return render(request, "accounts/profile.html", context={"form": form,
                                                             "addresses": addresses})
@login_required
def set_default_shipping(request, pk):
    address: ShippingAddress = get_object_or_404(ShippingAddress, pk=pk)
    address.set_default()
    return redirect("accounts:profile")

@login_required
def delete_address(request, pk):
    address = get_object_or_404(ShippingAddress, pk=pk, user=request.user)
    address.delete()
    return redirect('accounts:profile')

