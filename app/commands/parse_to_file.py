"""CLI: extract tenders from rostender.info and save to .db or .csv."""

import asyncio
import csv
import os

import typer

from app.database import Database
from app.scraper import RostenderScraper
from app.schemas import TenderModel

extractor_app = typer.Typer()


async def async_extract(max_items: int, output: str) -> list[TenderModel]:
    """Scrape up to max_items tenders and optionally save to file. Returns scraped list."""
    scraper = RostenderScraper()
    data = await scraper.scrape(max_items)

    output_dir = "data"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, output)
    ext = os.path.splitext(output)[1].lower()

    if ext == ".db":
        db = Database(db_path=output_path)
        await db.save_to_db(data)
        print(f"Данные сохранены в БД: {output_path}")
    elif ext == ".csv":
        with open(output_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=list(TenderModel.model_fields.keys()))
            writer.writeheader()
            for item in data:
                writer.writerow(item.model_dump())
        print(f"Данные сохранены в CSV: {output_path}")
    else:
        print("Неизвестный формат файла. Используйте .db или .csv")

    return data


@extractor_app.command("extract")
def extract(max: int = 10, output: str = "tenders.db"):
    """Scrape tenders and save to data/<output> (.db or .csv)."""
    asyncio.run(async_extract(max, output))
