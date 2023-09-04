import os
from datetime import datetime

import django
import pytest
from freezegun import freeze_time

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "workout.settings")
django.setup()
from rest_framework.test import APIClient  # noqa


@pytest.fixture()
def User():
    from api.models import User

    return User


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
def client_other_user(User):
    return User.objects.create_user(
        email="user2@mail.com",
        username="testuser2",
        password="password2",
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
def api_client_other_user(client_other_user):
    client = APIClient()
    client.force_authenticate(user=client_other_user)
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
    Muscle.objects.create(name="quadriceps")

    return Muscle


@pytest.fixture()
def Force():
    from api.models import Force

    Force.objects.create(name="pull")
    Force.objects.create(name="push")
    Force.objects.create(name="static")

    return Force


@pytest.fixture()
def Exercise(Level, Category, Mechanic, Equipment, Force):
    from api.models import Exercise

    Exercise.objects.create(
        id=1,
        name="Press Sit-Up",
        instructions="steps to do it",
        category=Category.objects.get(name="strength"),
        mechanic=Mechanic.objects.get(name="compound"),
        equipment=Equipment.objects.get(name="barbell"),
        level=Level.objects.get(name="Expert"),
        force=Force.objects.get(name="pull"),
    )

    Exercise.objects.create(
        id=2,
        name="Deadlift with Chains",
        instructions="steps to do it",
        category=Category.objects.get(name="strength"),
        mechanic=Mechanic.objects.get(name="compound"),
        equipment=Equipment.objects.get(name="barbell"),
        level=Level.objects.get(name="Expert"),
        force=Force.objects.get(name="pull"),
    )

    Exercise.objects.create(
        id=3,
        name="Barbell Squat To A Bench",
        instructions="steps to do it",
        category=Category.objects.get(name="strength"),
        mechanic=Mechanic.objects.get(name="compound"),
        equipment=Equipment.objects.get(name="barbell"),
        level=Level.objects.get(name="Expert"),
        force=Force.objects.get(name="push"),
    )

    return Exercise


@pytest.fixture()
def MusclePerExercise(Muscle, Exercise):
    from api.models import MusclePerExercise

    MusclePerExercise.objects.create(
        muscle=Muscle.objects.get(name="quadriceps"),
        exercise=Exercise.objects.get(name="Barbell Squat To A Bench"),
        is_primary_muscle=True,
    )

    MusclePerExercise.objects.create(
        muscle=Muscle.objects.get(name="forearms"),
        exercise=Exercise.objects.get(name="Deadlift with Chains"),
        is_primary_muscle=False,
    )

    MusclePerExercise.objects.create(
        muscle=Muscle.objects.get(name="abs"),
        exercise=Exercise.objects.get(name="Press Sit-Up"),
        is_primary_muscle=True,
    )

    MusclePerExercise.objects.create(
        muscle=Muscle.objects.get(name="shoulders"),
        exercise=Exercise.objects.get(name="Press Sit-Up"),
        is_primary_muscle=False,
    )


@pytest.fixture()
@freeze_time("2023-01-01")
def Workout(Exercise, client_user):
    from api.models import Workout

    Workout.objects.create(
        id=1,
        created=datetime.now(),
        user=client_user,
    )

    Workout.objects.create(
        id=2,
        created=datetime.now(),
        user=client_user,
    )

    return Workout


@pytest.fixture()
def WorkoutExercise(Workout, Exercise):
    from api.models import WorkoutExercise

    WorkoutExercise.objects.create(
        workout=Workout.objects.get(id=1),
        exercise=Exercise.objects.get(name="Barbell Squat To A Bench"),
    )

    WorkoutExercise.objects.create(
        workout=Workout.objects.get(id=1),
        exercise=Exercise.objects.get(name="Deadlift with Chains"),
    )

    return WorkoutExercise


@pytest.fixture()
def FavoriteExercise(User, Exercise):
    from api.models import FavoriteExercise

    return FavoriteExercise


@pytest.fixture()
def ExerciseLog(User, Exercise):
    from api.models import ExerciseLog

    return ExerciseLog


@pytest.fixture()
def WorkoutSession(User, Exercise, Workout):
    from api.models import WorkoutSession

    return WorkoutSession
