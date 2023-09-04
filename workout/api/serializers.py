from django.contrib.auth.password_validation import validate_password
from django.db.models import F, Max
from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied
from rest_framework.validators import UniqueValidator
from .helpers import get_filtered_exercises, get_queries
from .models import (
    Category,
    Equipment,
    Exercise,
    ExerciseLog,
    FavoriteExercise,
    Force,
    Image,
    Level,
    Mechanic,
    Muscle,
    User,
    Workout,
    WorkoutExercise,
    WorkoutSession,
)


class MuscleGroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Muscle
        fields = ["id", "name"]


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]


class MechanicSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Mechanic
        fields = ["id", "name"]


class EquipmentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Equipment
        fields = ["id", "name"]


class LevelSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Level
        fields = ["id", "name"]


class ForceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Force
        fields = ["id", "name"]


class ExerciseSerializer(serializers.HyperlinkedModelSerializer):
    category = CategorySerializer()
    mechanic = MechanicSerializer()
    equipment = EquipmentSerializer()
    level = LevelSerializer()
    force = ForceSerializer()
    primary_muscles = MuscleGroupSerializer(many=True)
    secondary_muscles = MuscleGroupSerializer(many=True)

    class Meta:
        model = Exercise
        fields = [
            "id",
            "name",
            "instructions",
            "category",
            "mechanic",
            "equipment",
            "level",
            "force",
            "primary_muscles",
            "secondary_muscles",
        ]


class ImageSerializer(serializers.HyperlinkedModelSerializer):
    exercise = ExerciseSerializer()

    class Meta:
        model = Image
        fields = ["id", "name", "exercise"]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email"]


class RegisterSerializer(serializers.HyperlinkedModelSerializer):
    email = serializers.EmailField(
        required=True, validators=[UniqueValidator(queryset=User.objects.all())]
    )

    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = (
            "username",
            "password",
            "confirm_password",
            "email",
            "first_name",
            "last_name",
        )
        extra_kwargs = {
            "first_name": {"required": True},
            "last_name": {"required": True},
        }

    def validate(self, attrs):
        if attrs["password"] != attrs["confirm_password"]:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data["username"],
            email=validated_data["email"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
        )

        user.set_password(validated_data["password"])
        user.save()

        return user


class ChangePasswordSerializer(serializers.HyperlinkedModelSerializer):
    old_password = serializers.CharField(write_only=True, required=True)
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ("old_password", "password", "confirm_password")

    def validate_old_password(self, value):
        user = self.context["request"].user
        if not user.check_password(value):
            raise serializers.ValidationError(
                {"old_password": "Old password is not correct"}
            )
        return value

    def validate(self, attrs):
        if attrs["password"] != attrs["confirm_password"]:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )

        return attrs

    def update(self, instance, validated_data):
        user = self.context["request"].user

        if user.pk != instance.pk:
            raise serializers.ValidationError(
                {"authorize": "You dont have permission for this user."}
            )

        instance.set_password(validated_data["password"])
        instance.save()

        return instance


class UpdateUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email")
        extra_kwargs = {
            "first_name": {"required": True},
            "last_name": {"required": True},
        }

    def validate_email(self, value):
        user = self.context["request"].user
        if User.objects.exclude(pk=user.pk).filter(email=value).exists():
            raise serializers.ValidationError({"email": "This email is not available."})
        return value

    def validate_username(self, value):
        user = self.context["request"].user
        if User.objects.exclude(pk=user.pk).filter(username=value).exists():
            raise serializers.ValidationError(
                {"username": "This username is not available."}
            )
        return value

    def update(self, instance, validated_data):
        user = self.context["request"].user

        if user.pk != instance.pk:
            raise serializers.ValidationError(
                {"authorize": "You dont have permission for this user."}
            )

        instance.first_name = validated_data["first_name"]
        instance.last_name = validated_data["last_name"]
        instance.email = validated_data["email"]
        instance.username = validated_data["username"]

        instance.save()

        return instance


class WorkoutSerializer(serializers.ModelSerializer):
    category = serializers.CharField(write_only=True, allow_blank=True, required=False)
    mechanic = serializers.CharField(write_only=True, allow_blank=True, required=False)
    equipment = serializers.CharField(write_only=True, allow_blank=True, required=False)
    level = serializers.CharField(write_only=True, allow_blank=True, required=False)
    force = serializers.CharField(write_only=True, allow_blank=True, required=False)
    muscles = serializers.ListField(write_only=True, required=False)
    exercises = ExerciseSerializer(read_only=True, many=True)
    id = serializers.IntegerField(read_only=True)
    user = UserSerializer(read_only=True)
    reps_per_exercise = serializers.SerializerMethodField()
    total_sets = serializers.SerializerMethodField()

    class Meta:
        model = Workout
        fields = [
            "id",
            "created",
            "exercises",
            "category",
            "mechanic",
            "equipment",
            "level",
            "force",
            "muscles",
            "reps_per_exercise",
            "total_sets",
            "is_favorite",
            "user",
        ]

    def create(self, validated_data):
        request_user = self.context["request"].user
        user = User.objects.get(id=request_user.id)
        queries = get_queries(data=validated_data)
        exercises = get_filtered_exercises(queries=queries)
        workout = Workout.objects.create(user=user)
        workout_exercises = []
        for exercise in exercises:
            workout_exercises.append(
                WorkoutExercise(workout=workout, exercise=exercise)
            )
        WorkoutExercise.objects.bulk_create(workout_exercises)
        return workout

    def get_reps_per_exercise(self, obj):
        workout = Workout.objects.get(id=obj.id)
        exercises = workout.exercises.all()
        return (
            Exercise.objects.filter(id__in=list(exercises.values_list("id", flat=True)))
            .annotate(
                total_reps=F("workouts_exercises__reps"),
            )
            .values("name", "total_reps")
        )

    def get_total_sets(self, obj):
        workout = Workout.objects.get(id=obj.id)
        exercises = workout.exercises.all()
        return (
            Exercise.objects.filter(id__in=list(exercises.values_list("id", flat=True)))
            .annotate(
                total_sets=F("workouts_exercises__sets"),
            )
            .values("total_sets")
        ).aggregate(Max("total_sets"))

    # TODO: investigate if these last two methods can be more efficient.

    def update(self, instance, validated_data):
        request_user = self.context["request"].user
        user = User.objects.get(id=request_user.id)
        if user.is_superuser or instance.user != user:
            raise PermissionDenied("Action not allowed")
        return super().update(instance, validated_data)


class FavoriteExerciseSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    exercise = ExerciseSerializer()

    class Meta:
        model = FavoriteExercise
        fields = ["user", "exercise"]


class ExerciseLogSerializer(serializers.ModelSerializer):
    exercise = ExerciseSerializer()
    sets_made = serializers.IntegerField()
    reps_per_set_made = serializers.ListField(child=serializers.IntegerField(), min_length=1, max_length=sets_made)
    weight_used = serializers.ListField(
        child=serializers.DecimalField(max_digits=5, decimal_places=2),
        allow_empty=True
    )

    class Meta:
        model = ExerciseLog
        fields = ["exercise", "sets_made", "reps_per_set_made", "weight_used"]


class WorkoutSessionSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    start_datetime = serializers.DateTimeField()
    end_datetime = serializers.DateTimeField()
    location = serializers.CharField()
    duration = serializers.SerializerMethodField()

    class Meta:
        model = WorkoutSession
        fields = ["user", "start_datetime", "end_datetime", "duration", "location"]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if instance.workout:
            data["workout"] = self.get_workout(instance)
        else:
            data["exercise_log"] = self.get_exercise_log(instance)
        return data

    def get_workout(self, obj: WorkoutSession):
        exercise_logs = ExerciseLog.objects.filter(workout_session_id=obj.id)
        workout_data = WorkoutSerializer(obj.workout).data
        exercise_logs_data = [ExerciseLogSerializer(log).data for log in exercise_logs]
        exercise_logs_dict = {log["exercise"]["id"]: log for log in exercise_logs_data}

        for exercise in workout_data["exercises"]:
            exercise_id = exercise["id"]
            if exercise_id in exercise_logs_dict:
                exercise["exercise_logs"] = {
                    "sets_made": exercise_logs_dict[exercise_id]["sets_made"],
                    "reps_per_set_made": exercise_logs_dict[exercise_id]["reps_per_set_made"],
                    "weight_used": exercise_logs_dict[exercise_id]["weight_used"],
                }

        return workout_data

    def get_duration(self, obj: WorkoutSession):
        duration = obj.end_datetime - obj.start_datetime
        return duration.total_seconds() / 60

    def get_exercise_log(self, obj: WorkoutSession):
        exercise_log = ExerciseLog.objects.get(workout_session_id=obj.id)
        return ExerciseLogSerializer(exercise_log).data
