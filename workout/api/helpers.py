import random
from django.db.models import Q
from .models import Exercise


def get_queries(data: dict()) -> Q:
    queries = Q()

    if data.get("category"):
        queries &= Q(category__name__iexact=data["category"])
    if data.get("mechanic"):
        queries &= Q(mechanic__name__iexact=data["mechanic"])
    if data.get("level"):
        queries &= Q(level__name__iexact=data["level"])
    if data.get("force"):
        queries &= Q(force__name__iexact=data["force"])
    if data.get("equipment"):
        queries &= Q(equipment__name__iexact=data["equipment"])
    if data.get("muscles"):
        muscles = [muscle.lower() for muscle in data["muscles"]]
        queries &= Q(muscle_per_exercise__muscle__name__in=muscles)

    return queries


def get_filtered_exercises(queries: Q) -> list[Exercise]:
    filtered_exercises = Exercise.objects.filter(queries)
    quantity = len(filtered_exercises) if len(filtered_exercises) < 10 else 10
    exercises = random.sample(list(filtered_exercises), k=quantity)

    return exercises
