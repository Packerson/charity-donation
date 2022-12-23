from django.contrib import admin

from .models import Donation, Institution
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group, User

# Remove Group form django admin panel
admin.site.unregister(Group)


"""Want to override delete action, 
    Delete user has to check:
        -if the user is admin and is it the last admin?
        -cannot delete myself
        -"""


class UserAdmin(UserAdmin):
    pass


# Register your models here.

admin.site.register(Donation)
admin.site.register(Institution)
