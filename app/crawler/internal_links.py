from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
import requests


def normalize_url(url):

    parsed = urlparse(url)

    path = parsed.path.rstrip("/")

    if path == "":
        path = "/"

    return (
        parsed.scheme
        + "://"
        + parsed.netloc
        + path
    )


def get_internal_links(url):

    try:

        response = requests.get(
            url,
            timeout=15,
            headers={
                "User-Agent": "SEO Audit Tool"
            }
        )

        soup = BeautifulSoup(
            response.text,
            "lxml"
        )

        base_domain = urlparse(url).netloc

        internal_links = set()

        internal_links.add(
            normalize_url(url)
        )

        for link in soup.find_all("a", href=True):

            href = link["href"]

            full_url = urljoin(
                url,
                href
            )

            parsed = urlparse(
                full_url
            )

            if parsed.netloc == base_domain:

                internal_links.add(
                    normalize_url(
                        full_url
                    )
                )

        return list(
            internal_links
        )

    except Exception:

        return []