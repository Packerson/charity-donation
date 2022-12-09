from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import check_password
from django.urls import reverse
from django.utils.text import slugify
from django.core.mail import EmailMessage


class SignUpForm(UserCreationForm):

    """USER CREATION FORM WITH EMAIL, PASSWORD, PASSWORD2 FIELDS
        EMAIL = USERNAME, CAN BE CHANGE IN USER SETTINGS """

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        """fields and attributes"""
        super(SignUpForm, self).__init__(*args, **kwargs)

        self.fields['email'].widget.attrs = {'class': 'form-group', 'placeholder': 'Email'}
        self.fields['password1'].widget.attrs = {'class': 'form-group', 'placeholder': 'Hasło'}
        self.fields['password2'].widget.attrs = {'class': 'form-group', 'placeholder': 'Powtórz hasło'}

    def send_email(self):
        email_subject = f"Witaj {self.clean_email()} "
        email_body = "Wciśnij link by aktywować konto"
        mail = EmailMessage(
            email_subject,
            email_body,
            'szachista49@wp.pl', # 'from@example.com', If omitted, the DEFAULT_FROM_EMAIL setting is used.
            # 'pawel.91.kaczmarek@gmail.com', # 'from@example.com', If omitted, the DEFAULT_FROM_EMAIL setting is used.
            ['pawel.dev.kaczmarek@gmail.com'], # to email

            reply_to=['szachista49@gmail.com'],
            headers={'Message-ID': 'foo'},
        )
        mail.send(fail_silently=False)
        print("wysłano maila")
        return mail

    def clean_email(self):
        email = self.cleaned_data['email']
        return email

    # def slug_generic(self):
    #     slug = slugify(self.clean_email())
    #     return reverse('User_profile', kwargs={"slug": self.clean_email()})

    def save(self, commit=True):

        """ EMAIL = USERNAME"""
        """need to rewrite username"""
        self.send_email()
        self.instance.username = self.clean_email()
        return super(SignUpForm, self).save()


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

