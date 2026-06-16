```python
def calculate_category_scores(pages):

    if not pages:
        return {
            "technical_score": 0,
            "onpage_score": 0,
            "content_score": 0,
            "eeat_score": 0,
            "local_seo_score": 0,
            "social_score": 0,
            "technical_breakdown": {},
            "onpage_breakdown": {}
        }

    total_pages = len(pages)

    missing_h1 = 0
    title_issues = 0
    description_issues = 0
    missing_alt = 0
    thin_content = 0
    missing_schema = 0
    technical_issues = 0

    eeat_total = 0
    local_total = 0
    social_total = 0
    internal_link_total = 0

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

        if page.get("missing_alt_images", 0) > 0:
            missing_alt += 1

        if page.get("word_count", 0) < 300:
            thin_content += 1

        if not page.get("schema_found"):
            missing_schema += 1

        if (
            not page.get("canonical")
            or page.get("noindex")
            or page.get("status_code", 200) >= 400
        ):
            technical_issues += 1

        eeat_total += page.get("eeat_score", 0)
        local_total += page.get("local_seo_score", 0)
        social_total += page.get("social_score", 0)
        internal_link_total += page.get("internal_link_score", 0)

    technical_score = 100
    onpage_score = 100
    content_score = 100

    technical_score -= round(
        (technical_issues / total_pages) * 20
    )

    onpage_score -= round(
        (
            (
                missing_h1
                + title_issues
                + description_issues
                + missing_alt
            )
            / total_pages
        ) * 10
    )

    content_score -= round(
        (thin_content / total_pages) * 20
    )

    technical_score = max(0, technical_score)
    onpage_score = max(0, onpage_score)
    content_score = max(0, content_score)

    avg_eeat = round(eeat_total / total_pages, 1)
    avg_local = round(local_total / total_pages, 1)
    avg_social = round(social_total / total_pages, 1)
    avg_internal = round(internal_link_total / total_pages, 1)

    title_score = max(
        0,
        100 - round((title_issues / total_pages) * 100)
    )

    description_score = max(
        0,
        100 - round((description_issues / total_pages) * 100)
    )

    heading_score = max(
        0,
        100 - round((missing_h1 / total_pages) * 100)
    )

    alt_score = max(
        0,
        100 - round((missing_alt / total_pages) * 100)
    )

    schema_score = max(
        0,
        100 - round((missing_schema / total_pages) * 100)
    )

    canonical_score = max(
        0,
        100 - round((technical_issues / total_pages) * 100)
    )

    return {
        "technical_score": technical_score,
        "onpage_score": onpage_score,
        "content_score": content_score,
        "eeat_score": avg_eeat,
        "local_seo_score": avg_local,
        "social_score": avg_social,

        "technical_breakdown": {
            "schema_score": schema_score,
            "canonical_score": canonical_score
        },

        "onpage_breakdown": {
            "title_score": title_score,
            "description_score": description_score,
            "heading_score": heading_score,
            "alt_score": alt_score,
            "internal_link_score": avg_internal
        }
    }
```
