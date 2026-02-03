"""Example client: fetches tenders from local API."""

import asyncio

import httpx

from app.config import get_settings


class TendersApiClient:
    """Async client for /tenders API."""

    def __init__(self) -> None:
        self.settings = get_settings()

    async def fetch_tenders(self, max_items: int | None = None) -> list:
        max_items = max_items or self.settings.max_items
        async with httpx.AsyncClient() as client:
            r = await client.get(
                f"{self.settings.base_url}/tenders/",
                params={"max_items": max_items},
            )
            r.raise_for_status()
            return r.json()


if __name__ == "__main__":
    client = TendersApiClient()
    tenders = asyncio.run(client.fetch_tenders())
    print(tenders)