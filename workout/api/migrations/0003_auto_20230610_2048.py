# Generated by Django 4.2.2 on 2023-06-10 20:48

import json
import os

from api.models import Exercise, Muscle, MusclePerExercise
from django.db import migrations


def load_data(apps, scheme_editor):
    migration_directory = os.path.dirname(os.path.abspath(__file__))
    json_file_path = os.path.join(migration_directory, "../exercises.json")

    with open(json_file_path) as file:
        exercises = json.load(file)
        for exercise in exercises:
            primary_muscle_names = exercise["primaryMuscles"]
            secondary_muscle_names = exercise["secondaryMuscles"]
            exercise_name = exercise["name"]
            exercise_object, _ = Exercise.objects.get_or_create(name=exercise_name)
            process_primary_muscle(
                exercise=exercise_object, primary_muscles=primary_muscle_names
            )

            process_secondary_muscle(
                exercise=exercise_object, secondary_muscles=secondary_muscle_names
            )


def process_primary_muscle(exercise: Exercise, primary_muscles: list[str]):
    for muscle_name in primary_muscles:
        muscle, _ = Muscle.objects.get_or_create(name=muscle_name)
        MusclePerExercise.objects.get_or_create(
            muscle=muscle, exercise=exercise, is_primary_muscle=1
        )


def process_secondary_muscle(exercise: Exercise, secondary_muscles: list[str]):
    for muscle_name in secondary_muscles:
        muscle, _ = Muscle.objects.get_or_create(name=muscle_name)
        MusclePerExercise.objects.get_or_create(
            muscle=muscle, exercise=exercise, is_primary_muscle=0
        )


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0002_auto_20230610_2047"),
    ]

    operations = [migrations.RunPython(load_data)]