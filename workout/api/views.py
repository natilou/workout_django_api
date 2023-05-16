from django_filters import rest_framework as filters
from rest_framework import viewsets

from .filters import ExerciseFilter
from .models import Category, Equipment, Exercise, Force, Level, Mechanic, Muscle
from .serializers import (
    CategorySerializer,
    EquipmentSerializer,
    ExerciseSerializer,
    ForceSerializer,
    LevelSerializer,
    MechanicSerializer,
    MuscleGroupSerializer,
)


class CategoryViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Category to be viewed or edited.
    """

    queryset = Category.objects.all().order_by("name")
    serializer_class = CategorySerializer


class EquipmentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Equipment to be viewed or edited.
    """

    queryset = Equipment.objects.all().order_by("name")
    serializer_class = EquipmentSerializer


class LevelViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Level to be viewed or edited.
    """

    queryset = Level.objects.all().order_by("name")
    serializer_class = LevelSerializer


class MechanicViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Mechanic to be viewed or edited.
    """

    queryset = Mechanic.objects.all().order_by("name")
    serializer_class = MechanicSerializer


class MuscleViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Muscle to be viewed or edited.
    """

    queryset = Muscle.objects.all().order_by("name")
    serializer_class = MuscleGroupSerializer


class ForceViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Force to be viewed or edited.
    """

    queryset = Force.objects.all().order_by("name")
    serializer_class = ForceSerializer


class ExerciseViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Exercise to be viewed or edited.
    """

    queryset = Exercise.objects.all().order_by("name")
    serializer_class = ExerciseSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = ExerciseFilter
