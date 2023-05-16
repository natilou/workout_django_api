import json

from api.models import Category, Equipment, Force, Level, Mechanic
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options) -> None:
        with open("./api/exercises.json") as file:
            exercises = json.load(file)
            exercises_list = []
            for index, exercise in enumerate(exercises, start=1):
                force = Force.objects.get(name=exercise["force"])
                level = Level.objects.get(name=exercise["level"])
                category = Category.objects.get(name=exercise["category"])
                equipment = Equipment.objects.get(name=exercise["equipment"])
                mechanic = Mechanic.objects.get(name=exercise["mechanic"])

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
