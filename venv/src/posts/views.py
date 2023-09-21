from django.shortcuts import render
from django.views.generic import ListView, DetailView

from posts.models import Articles


# Create your views here.
def about(request):
    return render(request, 'posts/about.html')

def communaute(request):
    return render(request, 'posts/communaute.html')

def home(request):
    return render(request, 'posts/home.html')

class DestinationListView(ListView):
    model = Articles
    context_object_name = 'destinations'
    template_name = 'posts/destinations_list.html'
    paginate_by = 3

class DestinationDetailView(DetailView):
    model = Articles
    context_object_name = 'destination'
    template_name = 'posts/destinations_detail.html'

