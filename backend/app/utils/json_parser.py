import json
import re


def extract_json(text: str):

    try:

        text = text.strip()

        # remove markdown blocks

        if "```json" in text:

            text = text.split(
                "```json"
            )[1].split(
                "```"
            )[0]

        elif "```" in text:

            text = text.split(
                "```"
            )[1]

        # extract first json object

        match = re.search(

            r'\{.*\}',

            text,

            re.DOTALL
        )

        if match:

            json_text = match.group()

            return json.loads(
                json_text
            )

    except Exception as e:

        print(
            "\nJSON PARSER ERROR:\n"
        )

        print(str(e))

    return {}