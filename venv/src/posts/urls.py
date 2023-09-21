
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from posts.views import DestinationListView, DestinationDetailView, about, home

app_name = "posts"

urlpatterns = [
    path('', home, name='home'),
    path('about/', about, name='about'),
    path('destination/', DestinationListView.as_view(), name='destinations_list'),
    path('destination/<str:slug>/', DestinationDetailView.as_view(), name='destinations_detail'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)