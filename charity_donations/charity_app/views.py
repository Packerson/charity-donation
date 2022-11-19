from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.views import View, generic
from django.views.generic.edit import CreateView

from charity_app.models import Donation


class LandingPage(View):
    """counter bags and institutions"""

    @staticmethod
    def count_bags_and_donated_institutions():
        donations = Donation.objects.all()
        bags_counter = 0
        institutions_array = []

        for donation in donations:
            bags_counter += donation.quantity
            if donation.institution not in institutions_array:
                institutions_array.append(donation.institution)

        institutions_counter = len(institutions_array)
        context = {'institutions_counter': institutions_counter,
                   'bags_counter': bags_counter}
        return context

    def get(self, request):
        context = self.count_bags_and_donated_institutions()
        return render(request, 'index.html', context)


class AddDonation(CreateView):
    model = Donation
    fields = '__all__'
    template_name = 'form.html'


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
            return redirect("Landing_page")
        else:
            messages.warning(request, "Mistake in login or password")
            return render(request, "login.html")


def logout_view(request):
    """logout view"""
    logout(request)
    return redirect("Landing_page")


class Register(generic.CreateView):
    form_class = UserCreationForm
    success_url = 'index.html'
    template_name = 'register.html'
