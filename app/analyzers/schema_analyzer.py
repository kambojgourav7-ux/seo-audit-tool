import json


def detect_schema_types(soup):

    schema_types = []

    schema_scripts = soup.find_all(
        "script",
        attrs={
            "type": "application/ld+json"
        }
    )

    for script in schema_scripts:

        try:

            if not script.string:
                continue

            data = json.loads(
                script.string
            )

            if isinstance(data, list):

                for item in data:

                    schema_type = item.get(
                        "@type"
                    )

                    if schema_type:

                        if isinstance(
                            schema_type,
                            list
                        ):

                            for t in schema_type:

                                if (
                                    t
                                    not in schema_types
                                ):
                                    schema_types.append(
                                        t
                                    )

                        else:

                            if (
                                schema_type
                                not in schema_types
                            ):
                                schema_types.append(
                                    schema_type
                                )

            elif isinstance(
                data,
                dict
            ):

                schema_type = data.get(
                    "@type"
                )

                if schema_type:

                    if isinstance(
                        schema_type,
                        list
                    ):

                        for t in schema_type:

                            if (
                                t
                                not in schema_types
                            ):
                                schema_types.append(
                                    t
                                )

                    else:

                        if (
                            schema_type
                            not in schema_types
                        ):
                            schema_types.append(
                                schema_type
                            )

        except Exception:
            continue

    return {

        "schema_types":
            schema_types,

        "schema_count":
            len(
                schema_types
            )
    }