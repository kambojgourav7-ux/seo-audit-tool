def analyze_technical_seo(page):

    issues = []

    canonical_present = bool(
        page.get(
            "canonical",
            ""
        )
    )

    noindex = page.get(
        "noindex",
        False
    )

    nofollow = page.get(
        "nofollow",
        False
    )

    status_code = page.get(
        "status_code",
        0
    )

    schema_found = page.get(
        "schema_found",
        False
    )

    indexable = (
        status_code == 200
        and not noindex
    )

    if not canonical_present:
        issues.append(
            "Missing canonical tag"
        )

    if noindex:
        issues.append(
            "Page is noindex"
        )

    if nofollow:
        issues.append(
            "Page is nofollow"
        )

    if status_code >= 400:
        issues.append(
            f"Status code {status_code}"
        )

    if not schema_found:
        issues.append(
            "No schema markup found"
        )

    return {
        "indexable": indexable,
        "canonical_present": canonical_present,
        "noindex": noindex,
        "nofollow": nofollow,
        "technical_issues": issues
    }