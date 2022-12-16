from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordChangeView
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail, BadHeaderError
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_str, force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views.generic import ListView
from django.views.generic.base import View
from django.views.generic.edit import CreateView, UpdateView

from charity_app.forms import SignUpForm, UserSettingsForm
from charity_app.models import Donation, Institution, Category
from charity_app.tokens import account_activation_token

"""
https://www.youtube.com/watch?v=xNqnHmXIuzU watch!

przycisk submit nie działa, pobrać go do js i zrobić submit

pobrać user.id z requesta i przesłać go do zapisu 


try data! in js 

js do wymiany! Uncaught TypeError: chosenCategories[0] is undefined
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


class ContactView(View):

    

    def post(self, request):


        admin_users = User.objects.filter(is_staff=True)
        admin_email_address = []
        for email_address in admin_users:
            admin_email_address.append(email_address.email)

        name = request.POST['name']
        surname = request.POST['surname']
        message_form = request.POST['message']
        username = request.user if request.user != "AnonymousUser" else ""
        print(username)

        email_subject = "Wiadomość wysłana przez formularz kontaktowy"
        email_message = render_to_string('contact_email.html', {
            'name': name,
            "surname": surname,
            'username': username,
            'message_form': message_form
        })

        """SEND EMAIL WITH DETAILS"""
        email_addresses = admin_email_address.append(request.user.email)
        print(admin_email_address)
        send_mail(
            email_subject,
            email_message,
            'info@sharpmind.club',
            email_addresses,
            fail_silently=False
        )
        print('wysłano maila kontaktowego')
        messages.success(request, "Wiadomość została wysłana przez formularz kontaktowy")

        return redirect('Landing_page')


class AddDonation(CreateView):
    model = Donation
    fields = ['quantity', 'categories', 'institution', 'address',
              'phone_number', 'city', 'zip_code',
              'pick_up_date', 'pick_up_time', 'user']
    template_name = 'form.html'
    success_url = reverse_lazy('Confirmation')

    @staticmethod
    def institutions_categories_method():
        institutions = Institution.objects.all()
        institutions_categories = []
        categories = []

        for institution in institutions:
            for category in institution.categories.all():
                categories.append(category.id)

            institutions_categories.append(str(categories))
            categories = []

        print(len(institutions_categories))
        return institutions_categories

    def get_context_data(self, **kwargs):
        context = super(AddDonation, self).get_context_data(**kwargs)
        categories = Category.objects.all()
        institutions = Institution.objects.all()
        context['categories'] = categories

        institutions_data = zip(institutions, self.institutions_categories_method())

        context['institutions'] = institutions_data

        return context


def confirmation_view(request):
    return render(request, 'form-confirmation.html')


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


class Register(View):
    """USER CREATION VIEW
    WITH EMAIL ACTIVATION LINK """

    form_class = SignUpForm
    # success_url = reverse_lazy('login')
    template_name = 'register.html'
    # success_message = "Your profile was created successfully"

    # def get_form_kwargs(self):
    #     """REQUEST SEND AS ARGUMENT TO FORM, THANKS THIS FORM HAS ACCESS TO USER OBJECT"""
    #
    #     kwargs = super().get_form_kwargs()
    #     kwargs.update({'request': self.request})
    #     return kwargs

    def get(self, request):
        """TEMPLATE VIEW"""
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        """FORM VIEW, """

        form = self.form_class(request.POST)
        if form.is_valid():
            """IF FORM VALID, 
            USER IS NOT ACTIVE"""

            user = form.save(commit=False)
            user.is_active = False  # Deactivate account till it is confirmed
            user.username = request.POST['email']
            user.save()

            current_site = get_current_site(request)
            email_subject = f"Witaj {user.email}"
            email_message = render_to_string('template_activation_account.html', {
                'user': user.email,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            """SEND EMAIL WITH DETAILS"""
            send_mail(
                email_subject,
                email_message,
                'info@sharpmind.club',
                ['szachista49@gmail.com'],  # to email na sztywno, [request.POST['email']],
                fail_silently=False)
            print("wysłano maila")
            messages.success(request, 'Aby ukończyć rejestrację, potwierdź email')

            return redirect('login')

        return render(request, self.template_name, {'form': form})


def activation(request, uidb64, token):

    """VIEW SET THANKS TO ACTIVATION LINK,
    DECODE UIDB64 AND TOKEN
    user_is_active = True"""

    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)

    except:
        user = None

    if user is not None and account_activation_token.check_token(user, token):

        """USER_ACTIVE = TRUE"""
        user.is_active = True
        user.save()

        messages.success(request, "Dziękuje za potwierdzenie konta, teraz możesz się zalogować")
        return redirect('login')

    else:
        messages.error(request, "Link aktywacyjny jest nieaktywny")
        return redirect('Landing_page')


class UserProfile(ListView):
    """PROFILE VIEW"""
    template_name = 'user_profile.html'
    model = Donation

    def get_context_data(self, object_list=None, **kwargs):
        """ GET USER ID TO COMPARE AND VALIDATE ACCESS """

        context = super(UserProfile, self).get_context_data(**kwargs)
        user_id = self.request.user.id
        context['user_id'] = user_id
        return context


class MyDonation(ListView):
    """VIEW FOR MY DONATION LIST, ORDER BY PICK UP DATE AND CREATION TIME"""

    template_name = 'my_donation.html'
    model = Donation
    ordering = ['pick_up_date', '-creation_time']

    def get_queryset(self):
        """SEND ONLY NON TAKEN DONATIONS"""

        queryset = Donation.objects.filter(user_id=self.request.user).filter(is_taken=False)
        return queryset

    def get_context_data(self, object_list=None, **kwargs):
        """ GET USER ID TO COMPARE AND VALIDATE ACCESS """
        """SEND THROUGH CONTEXT TAKEN INSTITUTIONS"""

        context = super(MyDonation, self).get_context_data(**kwargs)
        user_id = self.request.user.id
        context['user_id'] = user_id
        context['institutions'] = Donation.objects.filter(user_id=self.request.user).filter(is_taken=True)
        return context


class UpdateDonation(UpdateView):
    """UPDATE 'IS TAKEN' FIELD """

    model = Donation
    fields = ('is_taken',)
    template_name = 'update_donation.html'
    success_url = reverse_lazy('Donation')

    """FILTER BY USER.ID TO CHECK OWNER"""

    def get_queryset(self):
        queryset = Donation.objects.filter(user_id=self.request.user)
        return queryset

    """ GET USER ID TO COMPARE AND VALIDATE ACCESS """

    def get_context_data(self, object_list=None, **kwargs):
        context = super(UpdateDonation, self).get_context_data(**kwargs)
        user_id = Donation.objects.filter(user_id=self.request.user).first().user_id
        context['user_id'] = user_id
        return context


class UserSettings(UpdateView):
    """BASE VIEW FOR UPDATE USER INFORMATION'S """

    model = User
    form_class = UserSettingsForm
    template_name = 'User_settings.html'
    success_url = reverse_lazy('User_profile')

    def get_context_data(self, object_list=None, **kwargs):
        """ GET USER ID TO COMPARE AND VALIDATE ACCESS """

        context = super(UserSettings, self).get_context_data(**kwargs)
        user_id = User.objects.get(id=self.request.user.id).id
        context['user_id'] = user_id

        return context

    def get_form_kwargs(self):
        """REQUEST SEND AS ARGUMENT TO FORM, THANKS THIS FORM HAS ACCESS TO USER OBJECT"""

        kwargs = super().get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs

    def get_object(self, queryset=None):
        """OBJECT TO GET INITIAL VALUE TO TEMPLATE"""

        return self.request.user


class ChangingPasswordView(PasswordChangeView):
    """VIEW FOR CHANGING PASSWORD , PASSWORDCHANGEFORM IS FROM DJANGO.AUTH"""

    # form_class = PasswordChangeView
    form_class = PasswordChangeForm
    template_name = 'password_change.html'
    success_url = reverse_lazy('password_success')

    def get_context_data(self, object_list=None, **kwargs):
        context = super(ChangingPasswordView, self).get_context_data(**kwargs)
        user_id = User.objects.get(id=self.request.user.id).id
        context['user_id'] = user_id

        return context


def password_success(request):
    """METHOD FOR REDIRECT AFTER SUCCESSFULLY CHANGING PASSWORD"""

    context = {'user_id': request.user.id}
    return render(request, "password_success.html", context)
