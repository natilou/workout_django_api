import json

from api.models import Category, Equipment, Force, Level, Mechanic
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options) -> None:
        with open("./api/exercises.json") as file:
            exercises = json.load(file)
            exercises_list = []
            for index, exercise in enumerate(exercises, start=1):
                force = (
                    Force.objects.get(name__iexact=exercise["force"])
                    if exercise.get("force") is not None
                    else None
                )
                level = Level.objects.get(name__iexact=exercise["level"])
                category = Category.objects.get(name__iexact=exercise["category"])
                equipment = (
                    Equipment.objects.get(name__iexact=exercise["equipment"])
                    if exercise.get("equipment") is not None
                    else None
                )
                mechanic = (
                    Mechanic.objects.get(name__iexact=exercise["mechanic"])
                    if exercise.get("mechanic") is not None
                    else None
                )

                exercises_list.append(
                    {
                        "model": "api.exercise",
                        "pk": index,
                        "fields": {
                            "name": exercise["name"],
                            "instructions": exercise["instructions"],
                            "force": force.id if force else None,
                            "level": level.id,
                            "category": category.id,
                            "equipment": equipment.id if equipment else None,
                            "mechanic": mechanic.id if mechanic else None,
                        },
                    }
                )

        json_file = open("./api/fixtures/exercises.json", "w")
        json_file.write(json.dumps(exercises_list))
