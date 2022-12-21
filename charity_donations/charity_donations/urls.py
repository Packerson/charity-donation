"""charity_donations URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin

"""login_required redirect to login"""
from django.contrib.auth.decorators import login_required
from django.urls import path
from django.contrib.auth import views as auth_view


from charity_app.views import LandingPage, AddDonation, login_view, \
    Register, logout_view, UserProfile, confirmation_view, MyDonation, UpdateDonation, \
    UserSettings, password_success, ChangingPasswordView, activation, ContactView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', LandingPage.as_view(), name='Landing_page'),

    path('adddonation/', login_required(AddDonation.as_view()), name='Add_donation'),
    path('confirmation/', confirmation_view, name='Confirmation'),
    path('Contact/', ContactView.as_view(), name='Contact'),
    path('donation/<int:pk>', login_required(UpdateDonation.as_view()), name='Update_donation'),

    path('login/', login_view, name='login'),
    path('logout', logout_view, name='logout'),
    path('register/', Register.as_view(), name='Register'),
    path('profile/', login_required(UserProfile.as_view()), name='User_profile'),
    path('donation/', login_required(MyDonation.as_view()), name='Donation'),
    path('profile/<int:pk>/', login_required(UserSettings.as_view()), name='User_settings'),
    path('profile/password/', ChangingPasswordView.as_view(), name='password_change'),
    path('profile/password/success', password_success, name='password_success'),
    path('activate/<uidb64>/<token>', activation, name='Activate'),

    path('reset_password/', auth_view.PasswordResetView.as_view(
        template_name='password_forget/password_reset.html'
    ), name='password_reset'),
    path('reset_password_sent/', auth_view.PasswordResetDoneView.as_view(
        template_name='password_forget/password_reset_sent.html'
    ), name='password_reset_done'),
    path('reset/<uidb64>/<token>', auth_view.PasswordResetConfirmView.as_view(
        template_name='password_forget/password_reset_form.html'
    ), name='password_reset_confirm'),
    path('reset_password_complete/', auth_view.PasswordResetCompleteView.as_view(
        template_name='password_forget/password_reset_form.html'
    ), name='password_reset_complete'),



]
