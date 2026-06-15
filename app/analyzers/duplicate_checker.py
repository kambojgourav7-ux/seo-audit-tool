def find_duplicates(pages):

    title_map = {}

    description_map = {}

    for page in pages:

        title = page.get(
            "title",
            ""
        ).strip()

        description = page.get(
            "meta_description",
            ""
        ).strip()

        if title:

            title_map.setdefault(
                title,
                []
            ).append(
                page["url"]
            )

        if description:

            description_map.setdefault(
                description,
                []
            ).append(
                page["url"]
            )

    duplicate_titles = []

    duplicate_descriptions = []

    for title, urls in title_map.items():

        if len(urls) > 1:

            duplicate_titles.append({
                "title": title,
                "urls": urls
            })

    for description, urls in description_map.items():

        if len(urls) > 1:

            duplicate_descriptions.append({
                "description": description,
                "urls": urls
            })

    return {
        "duplicate_titles": duplicate_titles,
        "duplicate_descriptions": duplicate_descriptions
    }