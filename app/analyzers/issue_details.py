def generate_issue_details(pages):

    issue_details = {

        "title_too_short": [],
        "title_too_long": [],

        "description_too_short": [],
        "description_too_long": [],

        "multiple_h1": [],

        "thin_content": [],

        "missing_alt": [],

        "missing_schema": []
    }

    for page in pages:

        title_length = page.get(
            "title_length",
            0
        )

        if title_length < 30:

            issue_details[
                "title_too_short"
            ].append({
                "url": page["url"],
                "length": title_length
            })

        elif title_length > 60:

            issue_details[
                "title_too_long"
            ].append({
                "url": page["url"],
                "length": title_length
            })

        description_length = page.get(
            "description_length",
            0
        )

        if (
            description_length > 0
            and description_length < 120
        ):

            issue_details[
                "description_too_short"
            ].append({
                "url": page["url"],
                "length": description_length
            })

        elif description_length > 160:

            issue_details[
                "description_too_long"
            ].append({
                "url": page["url"],
                "length": description_length
            })

        if page.get(
            "h1_count",
            0
        ) > 1:

            issue_details[
                "multiple_h1"
            ].append({
                "url": page["url"],
                "count": page[
                    "h1_count"
                ]
            })

        if page.get(
            "word_count",
            0
        ) < 300:

            issue_details[
                "thin_content"
            ].append({
                "url": page["url"],
                "word_count":
                    page[
                        "word_count"
                    ]
            })

        if page.get(
            "missing_alt_images",
            0
        ) > 0:

            issue_details[
                "missing_alt"
            ].append({
                "url": page["url"],
                "missing_alt_images":
                    page[
                        "missing_alt_images"
                    ]
            })

        if not page.get(
            "schema_found"
        ):

            issue_details[
                "missing_schema"
            ].append({
                "url": page["url"]
            })

    return issue_details