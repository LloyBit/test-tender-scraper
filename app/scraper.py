"""Async scraper for rostender.info using parser."""

import asyncio
import re
from math import ceil

import httpx

from app.parser import RostenderParser
from app.schemas import TenderModel


BASE_URL = "https://rostender.info/extsearch?page=1"
TIMEOUT = 10.0


class RostenderScraper:
    """Fetches pages and parses tenders via RostenderParser."""

    def __init__(self, client: httpx.AsyncClient | None = None):
        self._client = client
        self._parser = RostenderParser()

    async def scrape(self, max_items: int) -> list[TenderModel]:
        """Scrape up to max_items tenders. Uses multiple pages if needed."""
        total_pages = ceil(max_items / RostenderParser.ITEMS_PER_PAGE)
        urls = [
            re.sub(r"page=\d+", f"page={i + 1}", BASE_URL)
            for i in range(total_pages)
        ]
        if self._client is not None:
            tasks = [self._client.get(u) for u in urls]
            responses = await asyncio.gather(*tasks, return_exceptions=True)
        else:
            async with httpx.AsyncClient(timeout=TIMEOUT) as client:
                tasks = [client.get(u) for u in urls]
                responses = await asyncio.gather(*tasks, return_exceptions=True)

        all_tenders = []
        for r in responses:
            if isinstance(r, Exception):
                continue
            try:
                r.raise_for_status()
                tenders = self._parser.parse_document(r.text)
                all_tenders.extend(tenders)
            except Exception:
                continue
            if len(all_tenders) >= max_items:
                break
        return all_tenders[:max_items]
