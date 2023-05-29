import pytest
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "workout.settings")
django.setup()
from rest_framework.test import APIClient  # noqa


@pytest.fixture()
def User(django_user_model):
    return django_user_model


@pytest.fixture()
def admin_user(User):
    return User.objects.create_user(
        email="admintest@admin.com",
        username="admintest",
        is_staff=True,
        is_superuser=True,
        password="password",
    )


@pytest.fixture()
def client_user(User):
    return User.objects.create_user(
        email="user@mail.com",
        username="testuser",
        password="password",
    )


@pytest.fixture()
def api_client_admin(admin_user):
    client = APIClient()
    client.force_authenticate(user=admin_user)
    return client


@pytest.fixture()
def api_client_user(client_user):
    client = APIClient()
    client.force_authenticate(user=client_user)
    return client


@pytest.fixture()
def Level():
    from api.models import Level

    Level.objects.create(name="Beginner")
    Level.objects.create(name="Intermediate")
    Level.objects.create(name="Expert")

    return Level


@pytest.fixture()
def Equipment():
    from api.models import Equipment

    Equipment.objects.create(name="bands")
    Equipment.objects.create(name="barbell")
    Equipment.objects.create(name="cable")
    Equipment.objects.create(name="kettlebells")
    Equipment.objects.create(name="machine")
    Equipment.objects.create(name="dumbbell")

    return Equipment


@pytest.fixture()
def Category():
    from api.models import Category

    Category.objects.create(name="cardio")
    Category.objects.create(name="plyometrics")
    Category.objects.create(name="powerlifting")
    Category.objects.create(name="strength")
    Category.objects.create(name="stretching")
    Category.objects.create(name="strongman")
    Category.objects.create(name="olympic weightlifting")

    return Category


@pytest.fixture()
def Mechanic():
    from api.models import Mechanic

    Mechanic.objects.create(name="compound")
    Mechanic.objects.create(name="isolation")

    return Mechanic


@pytest.fixture()
def Muscle():
    from api.models import Muscle

    Muscle.objects.create(name="abductors")
    Muscle.objects.create(name="abs")
    Muscle.objects.create(name="biceps")
    Muscle.objects.create(name="chest")
    Muscle.objects.create(name="forearms")
    Muscle.objects.create(name="glutes")
    Muscle.objects.create(name="lats")
    Muscle.objects.create(name="triceps")
    Muscle.objects.create(name="shoulders")
    Muscle.objects.create(name="neck")

    return Muscle


@pytest.fixture()
def Force():
    from api.models import Force

    Force.objects.create(name="pull")
    Force.objects.create(name="push")
    Force.objects.create(name="static")

    return Force
