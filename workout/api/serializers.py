from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Category, Equipment, Exercise, Force, Image, Level, Mechanic, Muscle


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


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email", "url"]


class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "password"]
