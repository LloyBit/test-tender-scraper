"""API: GET /tenders returns scraped tenders as JSON."""

from fastapi import APIRouter

from app.commands.parse_to_file import async_extract
from app.scraper import RostenderScraper

router = APIRouter(prefix="/tenders")


@router.get("/")
async def get_tenders(max_items: int = 10):
    """Scrape rostender.info and return tenders as JSON. No temp files."""
    scraper = RostenderScraper()
    data = await scraper.scrape(max_items)
    return [t.model_dump() for t in data]
