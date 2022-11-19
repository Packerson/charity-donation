import datetime
import random

from django.contrib.auth.models import User
from faker import Faker

from charity_app.models import Donation, Institution, Category

faker = Faker('en_US')

Institution_CHOICES = (
    ('FDN', "Foundation"),
    ('NGO', 'Non-governmental organization'),
    ('L-CALL', 'Local collection')
)

pick_up_date_CHOICES = (
    (datetime.date(2023, 10, 28)),
    (datetime.date(2023, 10, 29)),
    (datetime.date(2023, 10, 30)),
    (datetime.date(2023, 10, 31))
)

pick_up_time_CHOICES = (
    (datetime.time(10, 10)),
    (datetime.time(11, 11)),
    (datetime.time(8, 8)),
    (datetime.time(7, 16))
)


def add_users():
    for i in range(5):
        User.objects.create_user(f'user{i}', f'user{i}@mail.com', f'surname{i}')


def add_category():
    Category.objects.create(name="Category 1")
    Category.objects.create(name="Category 2")
    Category.objects.create(name="Category 3")
    Category.objects.create(name="Category 4")


def add_institution():
    for i in range(50):
        Institution.objects.create(name=faker.name(),
                                   description=faker.paragraph(nb_sentences=1),
                                   type=random.choice(Institution_CHOICES),
                                   # categories=set(random.choice(list(Category.objects.all()))))
                                   )


def add_donation():
    for i in range(80):
        Donation.objects.create(quantity=i,
                                # categories=random.choice(Category.objects.all()),
                                institution=random.choice(Institution.objects.all()),
                                address=faker.address(),
                                phone_number=random.randint(111111111,999999999),
                                city=faker.city(),
                                zip_code=faker.postcode(),
                                pick_up_date=random.choice(pick_up_date_CHOICES),
                                pick_up_time=random.choice(pick_up_time_CHOICES),
                                user=random.choice(User.objects.all()))


def add_categories_to_institutions():
    institutions = Institution.objects.all()
    categories = Category.objects.all().first()

    for institution in institutions:
        institution.categories.add(Category.objects.all().first().id)


def add_categories_to_donations():
    donations = Donation.objects.all()
    categories = Category.objects.all()

    for donation in donations:
        donation.categories.add(random.choice(Category.objects.all()).id)
