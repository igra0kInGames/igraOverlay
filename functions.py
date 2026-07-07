import json
import os


def import_from_json(filename):
    if not os.path.exists(filename) or os.path.getsize(filename) == 0:
        return {}

    try:
        with open(filename, 'r', encoding='utf-8') as file:
            return json.load(file)
    except json.JSONDecodeError:
        return {}


def dump_to_json(data, name_file):
    with open(name_file, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
