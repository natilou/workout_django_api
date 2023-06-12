import json
import sys

from .constants import models


def read_json(field: str) -> None:
    with open("./exercises.json") as file:
        exercises = json.load(file)

        attributes = set(
            data.get(field)[0] if isinstance(data.get(field), list) else data.get(field)
            for data in exercises
        )

        list_attributes_model = [
            {
                "model": models.get(field),
                "pk": index,
                "fields": {
                    "name": attribute[0] if isinstance(attribute, list) else attribute
                },
            }
            for index, attribute in enumerate(attributes, start=1)
            if attribute
        ]

        json_file = open(f"./fixtures/{field}.json", "w")
        json_file.write(json.dumps(list_attributes_model))


if __name__ == "__main__":
    field = sys.argv[1]
    read_json(field)
