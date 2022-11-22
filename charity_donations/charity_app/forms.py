from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User



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
        
    def save(self, commit=True):
        """need to rewrite username"""
        self.instance.username = self.clean_email()
        return super(SignUpForm, self).save()
        
