from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import check_password
from django.urls import reverse
from django.utils.text import slugify


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        """fields and attributes"""
        super(SignUpForm, self).__init__(*args, **kwargs)

        self.fields['email'].widget.attrs = {'class': 'form-group', 'placeholder': 'Email'}
        self.fields['password1'].widget.attrs = {'class': 'form-group', 'placeholder': 'Hasło'}
        self.fields['password2'].widget.attrs = {'class': 'form-group', 'placeholder': 'Powtórz hasło'}

    def clean_email(self):
        email = self.cleaned_data['email']
        return email

    def slug_generic(self):
        slug = slugify(self.clean_email())
        return reverse('User_profile', kwargs={"slug": self.clean_email()})

    def save(self, commit=True):
        """need to rewrite username"""
        self.instance.username = self.clean_email()
        return super(SignUpForm, self).save()


class UserSettingsForm(forms.ModelForm):
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
        password = self.cleaned_data['password']
        print(password)
        return password

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

    def save(self, commit=True):
        """need to rewrite username"""
        if authenticate(username=self.user.email, password=self.clean_password()):
            print('działa')
            return super(UserSettingsForm, self).save()
        else:
            print("nie działa")
            return ValidationError('Hasło nieprawidłowe')
