from app.utils.json_loader import (
    load_json_file
)

TRANSPORT_FILE = (
    "app/mock_server/transport_options.json"
)


def get_transport_options(
    city
):

    transports = load_json_file(
        TRANSPORT_FILE
    )

    results = []

    for transport in transports:

        if (
            transport["city"].lower()
            ==
            city.lower()
        ):

            results.append(
                transport
            )

    return results