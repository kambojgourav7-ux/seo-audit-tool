import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

from app.crawler.internal_links import get_internal_links

from app.analyzers.seo_score import calculate_seo_score
from app.analyzers.duplicate_checker import find_duplicates
from app.analyzers.site_summary import calculate_site_summary
from app.analyzers.technical_analyzer import analyze_technical_seo
from app.analyzers.category_scores import calculate_category_scores
from app.analyzers.issue_details import generate_issue_details
from app.analyzers.eeat_analyzer import analyze_eeat
from app.analyzers.social_analyzer import analyze_social_links
from app.analyzers.schema_analyzer import detect_schema_types
from app.analyzers.local_seo_analyzer import analyze_local_seo
from app.analyzers.nap_analyzer import analyze_nap
from app.analyzers.internal_link_analyzer import analyze_internal_links


def crawl_site(url):

    links = get_internal_links(url)

    domain = urlparse(
        url
    ).netloc.lower()

    pages = []

    for link in links[:100]:

        try:

            response = requests.get(
                link,
                timeout=15,
                headers={
                    "User-Agent": "SEO Audit Tool"
                }
            )

            soup = BeautifulSoup(
                response.text,
                "lxml"
            )

            title = ""

            if soup.title:

                title = soup.title.get_text(
                    strip=True
                )

            meta_description = ""

            meta = soup.find(
                "meta",
                attrs={
                    "name": "description"
                }
            )

            if meta:

                meta_description = meta.get(
                    "content",
                    ""
                )

            h1_tags = soup.find_all(
                "h1"
            )

            h2_tags = soup.find_all(
                "h2"
            )

            canonical = ""

            canonical_tag = soup.find(
                "link",
                rel="canonical"
            )

            if canonical_tag:

                canonical = canonical_tag.get(
                    "href",
                    ""
                )

            robots_meta = soup.find(
                "meta",
                attrs={
                    "name": "robots"
                }
            )

            robots_content = ""

            if robots_meta:

                robots_content = robots_meta.get(
                    "content",
                    ""
                ).lower()

            noindex = (
                "noindex" in robots_content
            )

            nofollow = (
                "nofollow" in robots_content
            )

            images = soup.find_all(
                "img"
            )

            missing_alt = 0

            for image in images:

                if not image.get(
                    "alt"
                ):

                    missing_alt += 1

            text_content = soup.get_text(
                separator=" ",
                strip=True
            )

            word_count = len(
                text_content.split()
            )

            schema_found = bool(
                soup.find(
                    "script",
                    attrs={
                        "type": "application/ld+json"
                    }
                )
            )

            schema_data = detect_schema_types(
                soup
            )

            page_data = {

                "url":
                    link,

                "status_code":
                    response.status_code,

                "title":
                    title,

                "title_length":
                    len(title),

                "meta_description":
                    meta_description,

                "description_length":
                    len(meta_description),

                "h1_count":
                    len(h1_tags),

                "h2_count":
                    len(h2_tags),

                "canonical":
                    canonical,

                "word_count":
                    word_count,

                "images_count":
                    len(images),

                "missing_alt_images":
                    missing_alt,

                "schema_found":
                    schema_found,

                "schema_types":
                    schema_data[
                        "schema_types"
                    ],

                "schema_count":
                    schema_data[
                        "schema_count"
                    ],

                "noindex":
                    noindex,

                "nofollow":
                    nofollow,

                "content_text":
                    text_content
            }

            page_data.update(
                calculate_seo_score(
                    page_data
                )
            )

            page_data.update(
                analyze_technical_seo(
                    page_data
                )
            )

            page_data.update(
                analyze_eeat(
                    page_data
                )
            )

            page_data.update(
                analyze_social_links(
                    soup
                )
            )

            page_data.update(
                analyze_local_seo(
                    soup,
                    page_data
                )
            )

            page_data.update(
                analyze_nap(
                    soup
                )
            )

            page_data.update(
                analyze_internal_links(
                    soup,
                    domain
                )
            )

            page_data.pop(
                "content_text",
                None
            )

            pages.append(
                page_data
            )

        except Exception as e:

            print(
                f"Error crawling {link}: {e}"
            )

            continue

    duplicates = find_duplicates(
        pages
    )

    site_summary = calculate_site_summary(
        pages
    )

    category_scores = calculate_category_scores(
        pages
    )

    issue_details = generate_issue_details(
        pages
    )

    return {

        "executive_summary":
            site_summary[
                "executive_summary"
            ],

        "warning_breakdown":
            site_summary[
                "warning_breakdown"
            ],

        "category_scores":
            category_scores,

        "issue_details":
            issue_details,

        "pages_crawled":
            len(
                pages
            ),

        "site_score":
            site_summary[
                "site_score"
            ],

        "summary":
            site_summary[
                "summary"
            ],

        "issue_pages":
            site_summary[
                "issue_pages"
            ],

        "pages":
            pages,

        "duplicate_titles":
            duplicates[
                "duplicate_titles"
            ],

        "duplicate_descriptions":
            duplicates[
                "duplicate_descriptions"
            ]
    }