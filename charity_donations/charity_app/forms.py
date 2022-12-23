from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext, gettext_lazy as _


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


"""Want to override widget for display two password inputs"""


# class SetPasswordForm(forms.Form):
#     """
#     A form that lets a user change set their password without entering the old
#     password
#     """
#     error_messages = {
#         'password_mismatch': _("The two password fields didn't match."),
#     }
#     new_password1 = forms.CharField(label=_("New password"),
#                                     widget=forms.PasswordInput())
#     new_password2 = forms.CharField(label=_("New password confirmation"),
#                                     widget=forms.PasswordInput())
#
#     def __init__(self, user, *args, **kwargs):
#         self.user = user
#         super(SetPasswordForm, self).__init__(*args, **kwargs)
#         self.fields['new_password1'].widget.attrs = {'class': 'form-group', 'placeholder':'Wpisz nowe hasło'}
#         self.fields['new_password2'].widget.attrs = {'class': 'form-group'}
#
#     def clean_new_password2(self):
#         password1 = self.cleaned_data.get('new_password1')
#         password2 = self.cleaned_data.get('new_password2')
#         if password1 and password2:
#             if password1 != password2:
#                 raise forms.ValidationError(
#                     self.error_messages['password_mismatch'],
#                     code='password_mismatch',
#                 )
#         return password2
#
#     def save(self, commit=True):
#         self.user.set_password(self.cleaned_data['new_password1'])
#         if commit:
#             self.user.save()
#         return self.user
