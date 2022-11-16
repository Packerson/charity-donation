from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.http import request
from django.shortcuts import render, redirect
from django.views import View, generic
from django.views.generic.edit import CreateView

from models import Donation

"""Add url, and change main in login"""


# Create your views here.

class LandingPage(View):

    def get(self):
        return render(request, 'index.html')


class AddDonation(CreateView):
    model = Donation
    fields = '__all__'


def login_view(request):
    """login view"""
    if request.method == "GET":
        return render(request, "login.html")
    else:
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, "Login!")
            return redirect("main")
        else:
            messages.warning(request, "Mistake in login or password")
            return render(request, "login.html")


def logout_view(request):
    """logout view"""
    logout(request)
    return redirect("main")


class Register(generic.CreateView):
    form_class = UserCreationForm
    # success_url =
    template_name = 'register.html'
