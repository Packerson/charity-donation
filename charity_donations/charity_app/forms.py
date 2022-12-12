from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.http import BadHeaderError
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from charity_app.tokens import account_activation_token


# def activate_email(request, to_email):
#     messages.success(request, f" , sprawdź email: {to_email},"
#                               f" i wejdź w link aktywacyjny ")


class SignUpForm(UserCreationForm):
    """USER CREATION FORM WITH EMAIL, PASSWORD, PASSWORD2 FIELDS
        EMAIL = USERNAME, CAN BE CHANGE IN USER SETTINGS """

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')

    def __init__(self, request, *args, **kwargs):
        """fields and attributes"""
        super(SignUpForm, self).__init__(*args, **kwargs)

        self.request = request
        self.fields['email'].widget.attrs = {'class': 'form-group', 'placeholder': 'Email'}
        self.fields['password1'].widget.attrs = {'class': 'form-group', 'placeholder': 'Hasło'}
        self.fields['password2'].widget.attrs = {'class': 'form-group', 'placeholder': 'Powtórz hasło'}

    def clean_email(self):
        email = self.cleaned_data['email']
        return email

    def save(self, commit=False):

        """ EMAIL = USERNAME"""
        """need to rewrite username"""

        self.instance.is_active = False
        self.instance.username = self.clean_email()
        super(SignUpForm, self).save()
        self.send_email(email=self.clean_email(), request=self.request)
        return super(SignUpForm, self)

    @staticmethod
    def send_email(email, request):
        user = User.objects.get(email=email)
        email_subject = f"Witaj {user.email} "
        email_body = render_to_string('template_activation_account.html',
                                      {
                                          'user': user.email,
                                          'domain': get_current_site(request).domain,
                                          'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                                          'token': account_activation_token.make_token(user),
                                          'protocol': 'https' if request.is_secure() else 'http'

                                      })
        try:
            send_mail(
                email_subject,
                email_body,
                #
                'info@sharpmind.club',  # 'from@example.com', If omitted, the DEFAULT_FROM_EMAIL setting is used.
                # 'pawel.91.kaczmarek@gmail.com', # 'from@example.com', If omitted, the DEFAULT_FROM_EMAIL setting is used.
                ['szachista49@gmail.com'],  # to email na sztywno

                # reply_to=['szachista49@gmail.com'],
                # headers={'Message-ID': 'foo'},
                fail_silently=False)
            # messages.success(requests, f"Aby aktywować konto sprawdź maila: {self.clean_email()} i kliknij w link aktywacyjny")
            print("wysłano maila")
            return email_subject

        except BadHeaderError:
            # messages.error(requests, "coś poszło nie tak")
            return email_subject


class UserSettingsForm(forms.ModelForm):
    """USER SETTINGS FORM, USER CAN ADD OR CHANGE HIS PROFILE,
        TO DO THAT NEED TO CONFIRM HIS PASSWORD"""

    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password')

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.user = request.user
        self.fields['username'].widget.attrs = {'class': 'form-group'}
        self.fields['email'].widget.attrs = {'class': 'form-group'}
        self.fields['first_name'].widget.attrs = {'class': 'form-group'}
        self.fields['last_name'].widget.attrs = {'class': 'form-group'}
        self.fields['password'].widget.attrs = {'class': 'form-group'}

    def clean_password(self):

        """VALIDATE ENTERED PASSWORD BY AUTHENTICATE """

        updated_user = authenticate(username=self.user.email,
                                    password=self.cleaned_data['password'])
        if updated_user:
            password = self.user.password

            return password

        raise forms.ValidationError('nieprawidłowe hasło')

    def clean_username(self):
        if not self.cleaned_data['username']:
            username = self.user.username
        else:
            username = self.cleaned_data['username']
        return username

    def clean_email(self):
        if not self.cleaned_data['email']:
            email = self.user.email
        else:
            email = self.cleaned_data['email']

        return email

    def clean_first_name(self):
        if not self.cleaned_data['first_name']:
            first_name = self.user.first_name
        else:
            first_name = self.cleaned_data['first_name']
        print(first_name)
        return first_name

    def clean_last_name(self):
        if not self.cleaned_data['last_name']:
            last_name = self.user.last_name
        else:
            last_name = self.cleaned_data['last_name']
        print(last_name)
        return last_name
