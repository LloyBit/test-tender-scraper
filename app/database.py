import re

import aiosqlite

from app.config import get_settings
from app.schemas import TenderModel


class Database:
    """Async SQLite wrapper for tenders. Optional db_path overrides config location."""

    def __init__(self, db_path: str | None = None):
        self.settings = get_settings()
        self.db_name = self.settings.db_name
        self.db_path = db_path if db_path is not None else self.settings.db_path
        self.table_name = "tenders"

    async def create_table(self) -> None:
        """Create tenders table if it does not exist."""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(f"""
                CREATE TABLE IF NOT EXISTS {self.table_name} (
                    number TEXT PRIMARY KEY,
                    start_date TEXT,
                    end_date TEXT,
                    title TEXT,
                    url TEXT,
                    region TEXT,
                    price TEXT
                )
            """)
            await db.commit()

    @staticmethod
    def clean(text: str | None) -> str | None:
        """Normalize whitespace in text."""
        if not isinstance(text, str):
            return text
        return re.sub(r'\s+', ' ', text).strip()

    async def insert_in_table(self, item: TenderModel) -> None:
        """Insert one tender row (or skip if number exists)."""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(f"""
                INSERT OR IGNORE INTO {self.table_name} (number, start_date, end_date, title, url, region, price)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                self.clean(item.number),
                self.clean(item.start_date),
                self.clean(item.end_date),
                self.clean(item.title),
                self.clean(item.url),
                self.clean(item.region),
                self.clean(item.price)
            ))
            await db.commit()

    async def save_to_db(self, data: list[TenderModel]) -> None:
        """Create table and insert all tenders."""
        await self.create_table()
        for item in data:
            await self.insert_in_table(item)

