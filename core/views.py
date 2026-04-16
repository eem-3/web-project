from django.shortcuts import render
<<<<<<< HEAD
from django.http import HttpResponse
def view_home(request):
    return render(request, 'home.html')
=======
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView

class SignUpView(CreateView):
    form_class = UserCreationForm                  # the form to show (username + password + confirm)
    template_name = 'registration/signup.html'     # the HTML template to render
    success_url = reverse_lazy('login')            # after signup, redirect to the login page

# Create your views here.
>>>>>>> main
