from django.urls import path, reverse_lazy
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import (PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView)

from accounts.views import account, create_account, logout_user
app_name = "accounts"

urlpatterns = [
    path('account/', account, name='account'),
    path('account/create_account/', create_account, name='create_account'),
    path('logout/', logout_user, name='logout'),

    path('password-reset/', PasswordResetView.as_view(template_name='accounts/password_reset.html', html_email_template_name='accounts/password_reset_email.html'), name='password-reset'),
    path('password_reset/done/', PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='accounts/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password-reset-complete/', PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'), name='password_reset_complete'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
