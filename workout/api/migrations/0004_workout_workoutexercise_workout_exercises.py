# Generated by Django 4.2.1 on 2023-05-26 01:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0003_auto_20230513_1502"),
    ]

    operations = [
        migrations.CreateModel(
            name="Workout",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name="WorkoutExercise",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("reps", models.IntegerField()),
                ("sets", models.IntegerField()),
                (
                    "exercise",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="workouts_exercises",
                        to="api.exercise",
                    ),
                ),
                (
                    "workout",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="workouts_exercises",
                        to="api.workout",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="workout",
            name="exercises",
            field=models.ManyToManyField(
                related_name="workouts",
                through="api.WorkoutExercise",
                to="api.exercise",
            ),
        ),
    ]