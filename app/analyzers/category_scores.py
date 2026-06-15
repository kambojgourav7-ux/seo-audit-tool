def calculate_category_scores(pages):

    if not pages:

        return {
            "technical_score": 0,
            "onpage_score": 0,
            "content_score": 0,
            "image_score": 0,
            "schema_score": 0
        }

    technical_score = 100
    onpage_score = 100
    content_score = 100
    image_score = 100
    schema_score = 100

    total_pages = len(pages)

    missing_h1 = 0
    title_issues = 0
    description_issues = 0

    thin_content = 0

    missing_alt = 0

    missing_schema = 0

    technical_issues = 0

    for page in pages:

        if page.get("h1_count", 0) == 0:
            missing_h1 += 1

        if (
            page.get("title_length", 0) < 30
            or page.get("title_length", 0) > 60
        ):
            title_issues += 1

        if (
            page.get("description_length", 0) < 120
            or page.get("description_length", 0) > 160
        ):
            description_issues += 1

        if page.get("word_count", 0) < 300:
            thin_content += 1

        if page.get("missing_alt_images", 0) > 0:
            missing_alt += 1

        if not page.get("schema_found"):
            missing_schema += 1

        if (
            not page.get("canonical")
            or page.get("noindex")
            or page.get("status_code") >= 400
        ):
            technical_issues += 1

    onpage_score -= round(
        ((missing_h1 + title_issues + description_issues)
        / max(total_pages, 1)) * 10
    )

    content_score -= round(
        (thin_content / max(total_pages, 1)) * 20
    )

    image_score -= round(
        (missing_alt / max(total_pages, 1)) * 20
    )

    schema_score -= round(
        (missing_schema / max(total_pages, 1)) * 20
    )

    technical_score -= round(
        (technical_issues / max(total_pages, 1)) * 20
    )

    return {

        "technical_score":
            max(0, technical_score),

        "onpage_score":
            max(0, onpage_score),

        "content_score":
            max(0, content_score),

        "image_score":
            max(0, image_score),

        "schema_score":
            max(0, schema_score)
    }