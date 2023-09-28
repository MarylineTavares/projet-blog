from django.contrib.auth import get_user_model, login, authenticate, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from accounts.forms import UserForm

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


