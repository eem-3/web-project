from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .models import Entity
from django.http import HttpResponse
from .forms import BootstrapUserCreationForm
from django.contrib.auth.decorators import login_required

def view_home(request):
    if request.user.is_authenticated:
        llista_entitats = Entity.objects.all()
        return render(request, 'components/home.html', {'entities': llista_entitats})
    else:
        return render(request, 'components/homedemo.html')

class SignUpView(CreateView):
    """Sign up view."""
    form_class = BootstrapUserCreationForm         # the form to show (username + password + confirm)
    template_name = 'registration/signup.html'     # the HTML template to render
    success_url = reverse_lazy('login')            # after signup, redirect to the login page