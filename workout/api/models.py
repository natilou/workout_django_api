from django.contrib.auth.models import User
from django.db import models
from django.db.models import CheckConstraint, Q, F, UniqueConstraint
from django.core.exceptions import ValidationError


class User(User):
    @property
    def favorite_exercises(self):
        return Exercise.objects.filter(favorite_exercises__user=self)

    @property
    def favorite_exercises_count(self) -> int:
        return self.favorite_exercises.count()

    @property
    def favorite_workouts(self):
        return Workout.objects.filter(user=self, is_favorite=True)

    @property
    def favorite_workouts_count(self) -> int:
        return self.favorite_workouts.count()


class Muscle(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        app_label = "api"


class Category(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        app_label = "api"


class Mechanic(models.Model):
    name = models.CharField(max_length=100, null=True)

    class Meta:
        app_label = "api"


class Equipment(models.Model):
    name = models.CharField(max_length=100, null=True)

    class Meta:
        app_label = "api"


class Level(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        app_label = "api"


class Force(models.Model):
    name = models.CharField(max_length=100, null=True)

    class Meta:
        app_label = "api"


class Exercise(models.Model):
    name = models.CharField(max_length=100)
    instructions = models.TextField(max_length=500, null=True)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="exercises"
    )
    mechanic = models.ForeignKey(
        Mechanic, on_delete=models.CASCADE, related_name="exercises", null=True
    )
    equipment = models.ForeignKey(
        Equipment, on_delete=models.CASCADE, related_name="exercises", null=True
    )
    level = models.ForeignKey(Level, on_delete=models.CASCADE, related_name="exercises")
    force = models.ForeignKey(Force, on_delete=models.CASCADE, related_name="exercises", null=True)

    @property
    def primary_muscles(self):
        return Muscle.objects.filter(
            muscle_per_exercise__exercise_id=self.id,
            muscle_per_exercise__is_primary_muscle=True,
        )

    @property
    def secondary_muscles(self):
        return Muscle.objects.filter(
            muscle_per_exercise__exercise_id=self.id,
            muscle_per_exercise__is_primary_muscle=False,
        )

    class Meta:
        app_label = "api"


class MusclePerExercise(models.Model):
    muscle = models.ForeignKey(
        Muscle, on_delete=models.CASCADE, related_name="muscle_per_exercise"
    )
    exercise = models.ForeignKey(
        Exercise, on_delete=models.CASCADE, related_name="muscle_per_exercise"
    )
    is_primary_muscle = models.BooleanField()


class Image(models.Model):
    path = models.FileField(upload_to="static/exercise_images/")
    exercise = models.ForeignKey(
        Exercise, on_delete=models.CASCADE, related_name="images"
    )

    class Meta:
        app_label = "api"


class Workout(models.Model):
    created = models.DateField(auto_now_add=True)
    exercises = models.ManyToManyField(
        Exercise, through="WorkoutExercise", related_name="workouts"
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="workouts", default=None
    )
    is_favorite = models.BooleanField(default=False)


class WorkoutExercise(models.Model):
    workout = models.ForeignKey(
        Workout, on_delete=models.CASCADE, related_name="workouts_exercises"
    )

    exercise = models.ForeignKey(
        Exercise, on_delete=models.CASCADE, related_name="workouts_exercises"
    )
    reps = models.IntegerField(default=5)
    sets = models.IntegerField(default=5)


class FavoriteExercise(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="favorite_exercises"
    )

    exercise = models.ForeignKey(
        Exercise, on_delete=models.CASCADE, related_name="favorite_exercises"
    )


class WorkoutSession(models.Model):
    LOCATION_GYM = "gym"
    LOCATION_HOME = "home"
    LOCATION_OUTDOOR = "outdoor"
    LOCATION_CHOICES = [
        (LOCATION_GYM, "Gym"),
        (LOCATION_HOME, "Home"),
        (LOCATION_OUTDOOR, "Outdoor")
    ]
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="workout_sessions", null=True, blank=True,
    )
    workout = models.ForeignKey(
        Workout, on_delete=models.CASCADE, related_name="workout_sessions", null=True, blank=True,
        )
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    location = models.CharField(
        max_length=10,
        choices=LOCATION_CHOICES,
        default=LOCATION_HOME,
    )

    class Meta:
        constraints = [
            CheckConstraint(
                check=Q(end_datetime__gt=F("start_datetime")),
                name="check_start_datime",
            ),
            UniqueConstraint(
                fields=["start_datetime"],
                name="unique_start_datetime",
            ),
        ]

    def save(self, *args, **kwargs) -> None:
        if self.workout:
            self.user = self.workout.user
        elif self.workout is None and self.user is None:
            raise ValidationError("Either the user id or workout id must be specified")
        super().save(*args, **kwargs)


class ExerciseLog(models.Model):
    exercise = models.ForeignKey(
        Exercise, on_delete=models.CASCADE, related_name="exercises_logs"
    )
    sets_made = models.IntegerField()
    reps_per_set_made = models.JSONField(default=[])
    weight_used = models.JSONField(default=[])
    workout_session = models.ForeignKey(
        WorkoutSession, on_delete=models.CASCADE, related_name="exercises_logs"
    )
