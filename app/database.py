import aiosqlite
import re
from .schemas import TenderModel

async def create_db(db_name="tenders.db"):
    async with aiosqlite.connect(db_name) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS tenders (
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

def clean(text):
    if not isinstance(text, str):
        return text
    return re.sub(r'\s+', ' ', text).strip()

async def insert_in_db(item: TenderModel, db_name="tenders.db"):
    async with aiosqlite.connect(db_name) as db:
        await db.execute("""
            INSERT OR IGNORE INTO tenders (number, start_date, end_date, title, url, region, price)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            clean(item.number),
            clean(item.start_date),
            clean(item.end_date),
            clean(item.title),
            clean(item.url),
            clean(item.region),
            clean(item.price)
        ))
        await db.commit()

async def save_to_db(data: list[TenderModel], db_name="tenders.db"):
    await create_db(db_name)
    for item in data:
        await insert_in_db(item, db_name)
