"""Import base built in django model USER"""
from django.contrib.auth.backends import ModelBackend, UserModel
from django.contrib.auth.models import User
from django.core.exceptions import MultipleObjectsReturned
from django.db import models
from django.db.models import Q


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Institution(models.Model):
    Institution_CHOICES = (
        ('FDN', "Foundation"),
        ('NGO', 'Non-governmental organization'),
        ('L-CALL', 'Local collection')
    )

    name = models.CharField(max_length=255)
    description = models.TextField()
    type = models.CharField(max_length=100, choices=Institution_CHOICES,
                            default='FDN')
    categories = models.ManyToManyField(Category)

    def __str__(self):
        return self.name


class Donation(models.Model):
    quantity = models.IntegerField()
    categories = models.ManyToManyField(Category)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    address = models.CharField(max_length=100)
    phone_number = models.IntegerField()
    city = models.CharField(max_length=100)
    zip_code = models.IntegerField()
    pick_up_date = models.DateField()
    pick_up_time = models.TimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True,
                             default=True)
    more_info = models.TextField(null=True)
    is_taken = models.BooleanField(default=False)


class Users(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)


"""OVERRIDE USER AUTHENTICATE , ALLOW TO LOGIN BY USERNAME OR EMAIL
    ALSO NEED TO IMPORT IN SETTINGS.PY """


class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:  # to allow authentication through email or username or any other field, modify the below statement
            user = UserModel.objects.get(Q(username__iexact=username) | Q(email__iexact=username))
        except UserModel.DoesNotExist:
            UserModel().set_password(password)
        except MultipleObjectsReturned:
            return User.objects.filter(email=username).order_by('id').first()
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user

    def get_user(self, user_id):
        try:
            user = UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None

        return user if self.user_can_authenticate(user) else None
