from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User


#
# Sign Up Form
class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        self.fields['email'].widget.attrs = {'class': 'form-group', 'placeholder': 'Email'}
        self.fields['password1'].widget.attrs = {'class': 'form-group', 'placeholder': 'Hasło'}
        self.fields['password2'].widget.attrs = {'class': 'form-group', 'placeholder': 'Powtórz hasło'}
