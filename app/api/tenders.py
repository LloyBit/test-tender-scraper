from fastapi import APIRouter
from app.commands.parse_to_file import async_extract
import csv
import os

router = APIRouter(prefix="/tenders")

@router.get("/")
async def get_tenders(max_items: int = 10):
    output = "api_tenders.csv"
    output_path = os.path.join("data", output)

    await async_extract(max=max_items, output=output)

    # Прочитать CSV и вернуть как JSON
    with open(output_path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        data = list(reader)
        
    os.remove(output_path)
    return data