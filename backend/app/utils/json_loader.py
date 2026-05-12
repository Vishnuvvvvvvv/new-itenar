import json
import os


BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)


def load_json_file(relative_path):

    full_path = os.path.join(
        BASE_DIR,
        relative_path
    )

    with open(full_path, "r") as file:

        data = json.load(file)

    return data