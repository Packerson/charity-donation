"""Import base built in django model USER"""
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.db import models




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


class Users(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
