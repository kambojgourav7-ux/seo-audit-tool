def analyze_internal_links(
    soup,
    current_domain
):

    internal_links = 0
    external_links = 0

    internal_urls = []

    external_urls = []

    for link in soup.find_all("a"):

        href = link.get(
            "href",
            ""
        )

        if not href:

            continue

        href_lower = href.lower()

        if (
            href_lower.startswith("#")
            or href_lower.startswith("tel:")
            or href_lower.startswith("mailto:")
            or href_lower.startswith("javascript:")
        ):
            continue

        if (
            current_domain in href_lower
            or href_lower.startswith("/")
        ):

            internal_links += 1

            if len(
                internal_urls
            ) < 20:

                internal_urls.append(
                    href
                )

        elif href_lower.startswith(
            "http"
        ):

            external_links += 1

            if len(
                external_urls
            ) < 20:

                external_urls.append(
                    href
                )

    score = 100

    issues = []

    if internal_links < 5:

        score -= 40

        issues.append(
            "Very low internal links"
        )

    elif internal_links < 15:

        score -= 20

        issues.append(
            "Low internal links"
        )

    if external_links > internal_links:

        score -= 10

        issues.append(
            "More external than internal links"
        )

    score = max(
        score,
        0
    )

    return {

        "internal_links":
            internal_links,

        "external_links":
            external_links,

        "internal_link_score":
            score,

        "internal_link_issues":
            issues,

        "sample_internal_links":
            internal_urls,

        "sample_external_links":
            external_urls
    }