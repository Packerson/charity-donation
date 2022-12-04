from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

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
        fields = ('username', 'email', 'password')

    def __init__(self,  *args, **kwargs):
        super().__init__(*args, **kwargs)


        self.fields['username'].widget.attrs = {'class': 'form-group'}
        self.fields['email'].widget.attrs = {'class': 'form-group'}
        self.fields['password'].widget.attrs = {'class': 'form-group'}


    def clean_password(self):
        password = self.cleaned_data['password']
        return password

    # def clean_password2(self):
    #     password2 = self.cleaned_data['password2']
    #     print(password2)
    #     return password2
    #
    # def save(self, commit=True):
    #     if self.clean_password() == self.clean_password2():
    #         return super(UserSettingsForm, self).save()
