import json

from api.models import Category, Equipment, Force, Level, Mechanic
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options) -> None:
        with open("./api/exercises.json") as file:
            exercises = json.load(file)
            exercises_list = []
            for index, exercise in enumerate(exercises, start=1):
                force = Force.objects.get(name__iexact=exercise["force"])
                level = Level.objects.get(name__iexact=exercise["level"])
                category = Category.objects.get(name__iexact=exercise["category"])
                equipment = Equipment.objects.get(name__iexact=exercise["equipment"])
                mechanic = Mechanic.objects.get(name__iexact=exercise["mechanic"])

                exercises_list.append(
                    {
                        "model": "api.exercise",
                        "pk": index,
                        "fields": {
                            "name": exercise["name"],
                            "instructions": exercise["instructions"],
                            "force": force.id,
                            "level": level.id,
                            "category": category.id,
                            "equipment": equipment.id,
                            "mechanic": mechanic.id,
                        },
                    }
                )

        json_file = open("./api/fixtures/exercises.json", "w")
        json_file.write(json.dumps(exercises_list))
