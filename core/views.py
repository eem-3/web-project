from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .models import Entity
from django.http import HttpResponse

def view_home(request):
    llista_entitats = Entity.objects.all()
    return render(request, 'home.html', {'entities': llista_entitats})

class SignUpView(CreateView):
    form_class = UserCreationForm                  # the form to show (username + password + confirm)
    template_name = 'registration/signup.html'     # the HTML template to render
    success_url = reverse_lazy('login')            # after signup, redirect to the login page


