import re
import json


def analyze_nap(soup):

    content = soup.get_text(
        separator=" ",
        strip=True
    )

    business_name = None
    phone = None
    email = None
    address = None

    # Try Schema First

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

            if isinstance(
                data,
                dict
            ):

                if not business_name:

                    business_name = data.get(
                        "name"
                    )

                if not phone:

                    phone = data.get(
                        "telephone"
                    )

                if not address:

                    address_data = data.get(
                        "address"
                    )

                    if isinstance(
                        address_data,
                        dict
                    ):

                        street = address_data.get(
                            "streetAddress",
                            ""
                        )

                        city = address_data.get(
                            "addressLocality",
                            ""
                        )

                        state = address_data.get(
                            "addressRegion",
                            ""
                        )

                        postal = address_data.get(
                            "postalCode",
                            ""
                        )

                        address = " ".join(
                            [
                                street,
                                city,
                                state,
                                postal
                            ]
                        ).strip()

        except Exception:
            continue

    # Fallback Business Name

    if not business_name:

        if soup.title:

            title = soup.title.get_text(
                strip=True
            )

            if "|" in title:

                business_name = (
                    title.split("|")[-1]
                    .strip()
                )

            else:

                business_name = title

    # Phone

    if not phone:

        phone_match = re.search(
            r"\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}",
            content
        )

        if phone_match:

            phone = phone_match.group()

    # Email

    email_match = re.search(
        r"[\w\.-]+@[\w\.-]+\.\w+",
        content
    )

    if email_match:

        email = email_match.group()

    # Address Fallback

    if not address:

        address_match = re.search(
            r"\d+\s+[A-Za-z0-9\s\.]+,\s*[A-Za-z\s]+,\s*[A-Z]{2}\s*\d{5}",
            content
        )

        if address_match:

            address = address_match.group()

    # Presence Score

    nap_presence_score = 0

    if business_name:
        nap_presence_score += 25

    if phone:
        nap_presence_score += 25

    if email:
        nap_presence_score += 25

    if address:
        nap_presence_score += 25

    # Quality Score

    nap_quality_score = 0

    missing_address_parts = []

    if business_name:
        nap_quality_score += 25

    if phone:
        nap_quality_score += 25

    if email:
        nap_quality_score += 25

    if address:

        address_score = 25

        address_lower = address.lower()

        city_found = False
        state_found = bool(
            re.search(
                r"\b[A-Z]{2}\b",
                address
            )
        )

        zip_found = bool(
            re.search(
                r"\b\d{5}\b",
                address
            )
        )

        if "," in address:
            city_found = True

        if not city_found:

            address_score -= 8

            missing_address_parts.append(
                "City"
            )

        if not state_found:

            address_score -= 8

            missing_address_parts.append(
                "State"
            )

        if not zip_found:

            address_score -= 9

            missing_address_parts.append(
                "ZIP Code"
            )

        nap_quality_score += max(
            address_score,
            0
        )

    nap_quality_score = round(
        nap_quality_score,
        1
    )

    return {

        "website_nap": {

            "business_name":
                business_name,

            "phone":
                phone,

            "email":
                email,

            "address":
                address
        },

        "nap_presence_score":
            nap_presence_score,

        "nap_quality_score":
            nap_quality_score,

        "business_name_found":
            business_name is not None,

        "phone_found":
            phone is not None,

        "email_found":
            email is not None,

        "address_found":
            address is not None,

        "missing_address_parts":
            missing_address_parts
    }