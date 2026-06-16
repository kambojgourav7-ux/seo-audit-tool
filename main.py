from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.crawler.site_crawler import crawl_site

app = FastAPI(
    title="SEO Audit Tool",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


class AuditRequest(BaseModel):
    url: str


@app.get("/")
def home():
    return {
        "status": "running",
        "message": "SEO Audit Tool API"
    }


@app.get("/test")
def test():
    return {
        "message": "test route working"
    }


@app.post("/crawl/site")
def crawl_site_route(request: AuditRequest):
    result = crawl_site(request.url)
    result["siteUrl"] = request.url
    return result