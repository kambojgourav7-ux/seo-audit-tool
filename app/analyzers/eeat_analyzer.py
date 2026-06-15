import re


def analyze_eeat(page):

    content = page.get(
        "content_text",
        ""
    ).lower()

    url = page.get(
        "url",
        ""
    ).lower()

    experience_score = 0
    expertise_score = 0
    authority_score = 0
    trust_score = 0

    experience_signals = []
    expertise_signals = []
    authority_signals = []
    trust_signals = []

    # EXPERIENCE

    if (
        "years of experience" in content
        or "40+ years" in content
        or "serving our community" in content
    ):

        experience_score += 30

        experience_signals.append(
            "Experience history detected"
        )

    if (
        "reviews" in content
        or "testimonials" in content
    ):

        experience_score += 20

        experience_signals.append(
            "Reviews/Testimonial signals found"
        )

    if (
        "gallery" in content
        or "project" in content
        or "completed roofing projects" in content
    ):

        experience_score += 20

        experience_signals.append(
            "Project portfolio detected"
        )

    if (
        "service area" in content
    ):

        experience_score += 10

        experience_signals.append(
            "Local service area coverage found"
        )

    # EXPERTISE

    if (
        "faq" in content
    ):

        expertise_score += 20

        expertise_signals.append(
            "FAQ section found"
        )

    if (
        "licensed" in content
    ):

        expertise_score += 20

        expertise_signals.append(
            "Licensed business"
        )

    if (
        "bonded" in content
    ):

        expertise_score += 15

        expertise_signals.append(
            "Bonded business"
        )

    if (
        "insured" in content
    ):

        expertise_score += 15

        expertise_signals.append(
            "Insured business"
        )

    if (
        "roofing contractor" in content
        or "roofing services" in content
    ):

        expertise_score += 20

        expertise_signals.append(
            "Industry expertise detected"
        )

    # AUTHORITY

    if page.get(
        "schema_found"
    ):

        authority_score += 40

        authority_signals.append(
            "Schema markup found"
        )

    if (
        "localbusiness" in content
        or "organization" in content
    ):

        authority_score += 20

        authority_signals.append(
            "Business entity signals detected"
        )

    if (
        "awards" in content
        or "accreditation" in content
    ):

        authority_score += 20

        authority_signals.append(
            "Awards/accreditation found"
        )

    # TRUST

    if (
        "privacy policy" in content
    ):

        trust_score += 20

        trust_signals.append(
            "Privacy policy found"
        )

    if (
        "terms of use" in content
    ):

        trust_score += 20

        trust_signals.append(
            "Terms page found"
        )

    if (
        "@" in content
    ):

        trust_score += 15

        trust_signals.append(
            "Email address found"
        )

    phone_pattern = re.search(
        r"\d{3}[-.\s]?\d{3}[-.\s]?\d{4}",
        content
    )

    if phone_pattern:

        trust_score += 20

        trust_signals.append(
            "Phone number found"
        )

    if (
        "mailing address" in content
        or "address:" in content
    ):

        trust_score += 15

        trust_signals.append(
            "Physical address found"
        )

    if (
        page.get(
            "status_code",
            0
        ) == 200
    ):

        trust_score += 10

    experience_score = min(
        experience_score,
        100
    )

    expertise_score = min(
        expertise_score,
        100
    )

    authority_score = min(
        authority_score,
        100
    )

    trust_score = min(
        trust_score,
        100
    )

    eeat_score = round(
        (
            experience_score
            + expertise_score
            + authority_score
            + trust_score
        ) / 4,
        1
    )

    return {

        "eeat_score":
            eeat_score,

        "experience_score":
            experience_score,

        "expertise_score":
            expertise_score,

        "authority_score":
            authority_score,

        "trust_score":
            trust_score,

        "experience_signals":
            experience_signals,

        "expertise_signals":
            expertise_signals,

        "authority_signals":
            authority_signals,

        "trust_signals":
            trust_signals
    }