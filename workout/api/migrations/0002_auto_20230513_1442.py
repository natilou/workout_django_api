# Generated by Django 4.2.1 on 2023-05-13 14:42

from django.core.management import call_command
from django.db import migrations


def load_data(apps, schema_editor):
    call_command("loaddata", "../fixtures/category.json", app_label="api")
    call_command("loaddata", "../fixtures/equipment.json", app_label="api")
    call_command("loaddata", "../fixtures/level.json", app_label="api")
    call_command("loaddata", "../fixtures/mechanic.json", app_label="api")
    call_command("loaddata", "../fixtures/primaryMuscles.json", app_label="api")
    call_command("loaddata", "../fixtures/force.json", app_label="api")
    call_command("loaddata", "../fixtures/exercises.json", app_label="api")


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0001_initial"),
    ]

    operations = [migrations.RunPython(load_data)]