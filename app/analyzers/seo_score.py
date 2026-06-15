def calculate_seo_score(page):

    score = 100

    critical = []
    warnings = []
    passed = []

    title_length = page.get(
        "title_length",
        0
    )

    if title_length == 0:

        score -= 20

        critical.append(
            "Missing title"
        )

    elif title_length < 30:

        score -= 5

        warnings.append(
            "Title too short"
        )

    elif title_length > 60:

        score -= 5

        warnings.append(
            "Title too long"
        )

    else:

        passed.append(
            "Title optimized"
        )

    description_length = page.get(
        "description_length",
        0
    )

    if description_length == 0:

        score -= 15

        critical.append(
            "Missing meta description"
        )

    elif description_length < 120:

        score -= 5

        warnings.append(
            "Meta description too short"
        )

    elif description_length > 160:

        score -= 5

        warnings.append(
            "Meta description too long"
        )

    else:

        passed.append(
            "Meta description optimized"
        )

    h1_count = page.get(
        "h1_count",
        0
    )

    if h1_count == 0:

        score -= 15

        critical.append(
            "Missing H1"
        )

    elif h1_count > 1:

        score -= 5

        warnings.append(
            f"Multiple H1 tags ({h1_count})"
        )

    else:

        passed.append(
            "Single H1 found"
        )

    word_count = page.get(
        "word_count",
        0
    )

    if word_count < 100:

        score -= 20

        critical.append(
            "Very thin content"
        )

    elif word_count < 300:

        score -= 10

        warnings.append(
            "Thin content"
        )

    else:

        passed.append(
            "Content length good"
        )

    if not page.get(
        "canonical"
    ):

        score -= 10

        critical.append(
            "Missing canonical"
        )

    else:

        passed.append(
            "Canonical present"
        )

    missing_alt = page.get(
        "missing_alt_images",
        0
    )

    if missing_alt > 0:

        score -= min(
            missing_alt,
            10
        )

        warnings.append(
            f"{missing_alt} images missing ALT text"
        )

    else:

        passed.append(
            "All images have ALT text"
        )

    if not page.get(
        "schema_found"
    ):

        score -= 5

        warnings.append(
            "No schema markup found"
        )

    else:

        passed.append(
            "Schema detected"
        )

    if score < 0:
        score = 0

    return {
        "seo_score": score,
        "critical_issues": critical,
        "warnings": warnings,
        "passed_checks": passed
    }