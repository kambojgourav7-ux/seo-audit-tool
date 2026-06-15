def calculate_site_summary(pages):

    if not pages:
        return {}

    total_score = 0

    missing_titles = []
    missing_descriptions = []
    missing_h1 = []
    missing_canonical = []
    pages_without_schema = []
    pages_with_missing_alt = []

    total_critical = 0
    total_warnings = 0

    warning_breakdown = {
        "title_too_short": 0,
        "title_too_long": 0,
        "description_too_short": 0,
        "description_too_long": 0,
        "multiple_h1": 0,
        "thin_content": 0,
        "missing_alt": 0,
        "no_schema": 0
    }

    for page in pages:

        total_score += page.get(
            "seo_score",
            0
        )

        total_critical += len(
            page.get(
                "critical_issues",
                []
            )
        )

        total_warnings += len(
            page.get(
                "warnings",
                []
            )
        )

        for warning in page.get(
            "warnings",
            []
        ):

            warning_lower = warning.lower()

            if "title too short" in warning_lower:
                warning_breakdown[
                    "title_too_short"
                ] += 1

            elif "title too long" in warning_lower:
                warning_breakdown[
                    "title_too_long"
                ] += 1

            elif "meta description too short" in warning_lower:
                warning_breakdown[
                    "description_too_short"
                ] += 1

            elif "meta description too long" in warning_lower:
                warning_breakdown[
                    "description_too_long"
                ] += 1

            elif "multiple h1" in warning_lower:
                warning_breakdown[
                    "multiple_h1"
                ] += 1

            elif "thin content" in warning_lower:
                warning_breakdown[
                    "thin_content"
                ] += 1

            elif "alt text" in warning_lower:
                warning_breakdown[
                    "missing_alt"
                ] += 1

            elif "schema" in warning_lower:
                warning_breakdown[
                    "no_schema"
                ] += 1

        if page.get(
            "title_length",
            0
        ) == 0:

            missing_titles.append(
                page["url"]
            )

        if page.get(
            "description_length",
            0
        ) == 0:

            missing_descriptions.append(
                page["url"]
            )

        if page.get(
            "h1_count",
            0
        ) == 0:

            missing_h1.append(
                page["url"]
            )

        if not page.get(
            "canonical"
        ):

            missing_canonical.append(
                page["url"]
            )

        if not page.get(
            "schema_found"
        ):

            pages_without_schema.append(
                page["url"]
            )

        if page.get(
            "missing_alt_images",
            0
        ) > 0:

            pages_with_missing_alt.append({
                "url": page["url"],
                "missing_alt_images":
                    page["missing_alt_images"]
            })

    site_score = round(
        total_score / len(pages),
        1
    )

    top_issues = []

    if len(missing_h1) > 0:
        top_issues.append(
            f"{len(missing_h1)} pages missing H1"
        )

    strengths = []

    if len(missing_titles) == 0:
        strengths.append(
            "All pages have title tags"
        )

    if len(missing_descriptions) == 0:
        strengths.append(
            "All pages have meta descriptions"
        )

    if len(pages_without_schema) == 0:
        strengths.append(
            "Schema markup found on all pages"
        )

    if len(missing_canonical) == 0:
        strengths.append(
            "Canonical tags present on all pages"
        )

    return {

        "site_score": site_score,

        "summary": {

            "missing_titles": len(
                missing_titles
            ),

            "missing_descriptions": len(
                missing_descriptions
            ),

            "missing_h1": len(
                missing_h1
            ),

            "missing_canonical": len(
                missing_canonical
            ),

            "pages_without_schema": len(
                pages_without_schema
            ),

            "pages_with_missing_alt": len(
                pages_with_missing_alt
            )
        },

        "warning_breakdown":
            warning_breakdown,

        "executive_summary": {

            "pages_crawled": len(
                pages
            ),

            "overall_score": site_score,

            "critical_issues": total_critical,

            "warnings": total_warnings,

            "top_issues": top_issues,

            "strengths": strengths
        },

        "issue_pages": {

            "missing_titles":
                missing_titles,

            "missing_descriptions":
                missing_descriptions,

            "missing_h1":
                missing_h1,

            "missing_canonical":
                missing_canonical,

            "pages_without_schema":
                pages_without_schema,

            "pages_with_missing_alt":
                pages_with_missing_alt
        }
    }