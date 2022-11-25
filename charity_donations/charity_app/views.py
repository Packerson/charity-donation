from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView

from charity_app.forms import SignUpForm
from charity_app.models import Donation, Institution, Category
from django.contrib.auth.models import User


"""
Javascript compare categories with Institutions
pagination
"""

"""
superuser:
admin
admin@admin.com
qazWSXedc123
"""
"""edcwsxqaz321"""

class LandingPage(ListView):
    model = Institution
    template_name = "index.html"
    # paginate_by = 4

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

    def get_context_data(self, **kwargs):
        context = super(LandingPage, self).get_context_data(**kwargs)
        context.update(self.count_bags_and_donated_institutions())
        context.update(self.landing_page_institutions())

        # paginator = Paginator(context[foundations], self.paginate_by)
        #
        # page = self.request.GET.get('page')
        #
        # try:
        #     file_exams = paginator.page(page)
        # except PageNotAnInteger:
        #     file_exams = paginator.page(1)
        # except EmptyPage:
        #     file_exams = paginator.page(paginator.num_pages)
        #
        # context['list_exams'] = file_exams
        return context


class AddDonation(CreateView):
    model = Donation
    fields = '__all__'
    template_name = 'form.html'

    def get_context_data(self, **kwargs):
        context = super(AddDonation, self).get_context_data(**kwargs)
        categories = Category.objects.all()
        institutions = Institution.objects.all()
        context['categories'] = categories
        context['institutions'] = institutions
        return context


def login_view(request):
    """login view"""
    if request.method == "GET":
        return render(request, "login.html")
    else:
        email = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(username=email, password=password)
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


class Register(CreateView):
    form_class = SignUpForm
    # model = User
    success_url = reverse_lazy('login')
    template_name = 'register.html'
    success_message = "Your profile was created successfully"


class UserProfile(DetailView):

    model = User
    template_name = 'user_profile.html'



