from fastapi import FastAPI
from pydantic import BaseModel
import requests
from bs4 import BeautifulSoup

app = FastAPI(
    title="SEO Audit Tool",
    version="1.0.0"
)

class AuditRequest(BaseModel):
    url: str


@app.get("/")
def home():
    return {
        "status": "running",
        "message": "SEO Audit Tool API"
    }


@app.post("/audit/start")
def audit_site(data: AuditRequest):

    try:

        response = requests.get(
            data.url,
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
            title = soup.title.get_text(strip=True)

        meta_description = ""

        meta = soup.find(
            "meta",
            attrs={"name": "description"}
        )

        if meta:
            meta_description = meta.get(
                "content",
                ""
            )

        h1 = ""

        h1_tag = soup.find("h1")

        if h1_tag:
            h1 = h1_tag.get_text(strip=True)

        return {
            "url": data.url,
            "status_code": response.status_code,
            "title": title,
            "meta_description": meta_description,
            "h1": h1
        }

    except Exception as e:

        return {
            "error": str(e)
        }