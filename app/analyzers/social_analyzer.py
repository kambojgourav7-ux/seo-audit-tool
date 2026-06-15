def analyze_social_links(soup):

    social_profiles = {

        "facebook": None,
        "instagram": None,
        "linkedin": None,
        "youtube": None,
        "twitter": None,
        "pinterest": None,
        "tiktok": None
    }

    links = soup.find_all("a")

    for link in links:

        href = link.get(
            "href",
            ""
        ).lower()

        if "facebook.com" in href:
            social_profiles[
                "facebook"
            ] = href

        elif "instagram.com" in href:
            social_profiles[
                "instagram"
            ] = href

        elif "linkedin.com" in href:
            social_profiles[
                "linkedin"
            ] = href

        elif "youtube.com" in href:
            social_profiles[
                "youtube"
            ] = href

        elif "twitter.com" in href or "x.com" in href:
            social_profiles[
                "twitter"
            ] = href

        elif "pinterest.com" in href:
            social_profiles[
                "pinterest"
            ] = href

        elif "tiktok.com" in href:
            social_profiles[
                "tiktok"
            ] = href

    found_count = len(
        [
            value
            for value in social_profiles.values()
            if value
        ]
    )

    social_score = min(
        found_count * 20,
        100
    )

    return {

        "social_profiles":
            social_profiles,

        "social_profiles_found":
            found_count,

        "social_score":
            social_score
    }