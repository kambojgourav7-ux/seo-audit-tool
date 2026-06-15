import re


def analyze_local_seo(soup, page):

    local_score = 0

    checks_passed = []

    warnings = []

    content = soup.get_text(
        separator=" ",
        strip=True
    )

    content_lower = content.lower()

    # Phone

    phone_found = bool(
        re.search(
            r"\d{3}[-.\s]?\d{3}[-.\s]?\d{4}",
            content
        )
    )

    if phone_found:

        local_score += 15

        checks_passed.append(
            "Phone number found"
        )

    else:

        warnings.append(
            "Phone number not found"
        )

    # Email

    email_found = bool(
        re.search(
            r"[\w\.-]+@[\w\.-]+\.\w+",
            content
        )
    )

    if email_found:

        local_score += 10

        checks_passed.append(
            "Email address found"
        )

    else:

        warnings.append(
            "Email address not found"
        )

    # Address

    address_found = (
        "address" in content_lower
        or "mailing address" in content_lower
    )

    if address_found:

        local_score += 15

        checks_passed.append(
            "Address found"
        )

    else:

        warnings.append(
            "Address not found"
        )

    # LocalBusiness Schema

    schema_types = page.get(
        "schema_types",
        []
    )

    if (
        "LocalBusiness" in schema_types
        or "RoofingContractor" in schema_types
    ):

        local_score += 20

        checks_passed.append(
            "LocalBusiness schema found"
        )

    else:

        warnings.append(
            "LocalBusiness schema missing"
        )

    # Google Map Detection

    map_found = False

    for iframe in soup.find_all(
        "iframe"
    ):

        src = iframe.get(
            "src",
            ""
        ).lower()

        if (
            "google.com/maps" in src
            or "google.com/maps/embed" in src
        ):

            map_found = True

            break

    if map_found:

        local_score += 15

        checks_passed.append(
            "Google Map embed found"
        )

    # GBP Link Detection

    gbp_link_found = False

    gbp_url = None

    for link in soup.find_all(
        "a"
    ):

        href = link.get(
            "href",
            ""
        )

        href_lower = href.lower()

        if (
            "maps.google" in href_lower
            or "maps.app.goo.gl" in href_lower
            or "g.page" in href_lower
        ):

            gbp_link_found = True

            gbp_url = href

            break

    # GBP Status

    if gbp_link_found:

        gbp_status = "confirmed"

        local_score += 15

        checks_passed.append(
            "GBP link found"
        )

    elif map_found:

        gbp_status = "possible"

        local_score += 10

        checks_passed.append(
            "GBP likely exists via map embed"
        )

    else:

        gbp_status = "not_found"

        warnings.append(
            "No GBP signal found"
        )

    # Service Area

    if (
        "service area"
        in content_lower
    ):

        local_score += 10

        checks_passed.append(
            "Service area found"
        )

    local_score = min(
        local_score,
        100
    )

    return {

        "local_seo_score":
            local_score,

        "phone_found":
            phone_found,

        "email_found":
            email_found,

        "address_found":
            address_found,

        "google_map_found":
            map_found,

        "gbp_status":
            gbp_status,

        "gbp_link_found":
            gbp_link_found,

        "gbp_url":
            gbp_url,

        "checks_passed":
            checks_passed,

        "local_seo_warnings":
            warnings
    }