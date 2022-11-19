from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.views import generic, View
from django.views.generic.edit import CreateView

from charity_app.models import Donation, Institution, Category


class LandingPage(View):
    """count bags and institutions"""

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

    @staticmethod
    def landing_page_institutions():

        """searching by institutions type and categories FOUNDATION"""

        foundations = Institution.objects.filter(type__contains='FDN')
        categories_foundations = []

        for institution in foundations:
            categories = [category.name for category in Category.objects.filter(institution=institution)]
            categories_foundations.append(", ".join(categories))

        foundations = zip(foundations, categories_foundations)

        """searching by institutions type and categories NON GOVERNMENT ORGANISATION"""

        non_g_o = Institution.objects.filter(type__contains='NGO')
        categories_non_g_o = []

        for institution in non_g_o:
            categories = [category.name for category in Category.objects.filter(institution=institution)]
            categories_non_g_o.append(", ".join(categories))

        non_g_o = zip(non_g_o, categories_non_g_o)

        """searching by institutions type and categories LOCAL COLLECTIONS"""
        local = Institution.objects.filter(type__contains='L-CALL')
        categories_local = []

        for institution in local:
            categories = [category.name for category in Category.objects.filter(institution=institution)]
            categories_local.append(", ".join(categories))

        local = zip(local, categories_local)

        context_2 = {'foundations': foundations, 'non_g_o': non_g_o, 'local': local}
        return context_2

    def get(self, request):
        context = self.count_bags_and_donated_institutions()
        context.update(self.landing_page_institutions())

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
