import asyncio
import httpx
from bs4 import BeautifulSoup as bs
import re
from math import ceil
from app.database import save_to_db
import typer
import os
import csv
import traceback
from ..schemas import TenderModel

# CLI-команда для извлечения и сохранения данных
extractor_app = typer.Typer()

# URL, с которого начинается парсинг
parse_url = "https://rostender.info/extsearch?page=1"

# Функция для парсинга одной тендерной записи
def parse_tender(tender, clean_page):

    # извлекаем целевые данные тендера
    number_tag = tender.find("span", class_="tender__number")
    number_text = number_tag.get_text(strip=True) if number_tag else ""
    number = number_text.split("№")[-1].strip() if "№" in number_text else None

    start_date = tender.find("span", class_="tender__date-start")
    start_date = start_date.get_text(strip=True).replace("от ", "") if start_date else None

    end_date_tag = tender.select_one("span.tender__date-end, span.black")
    end_date = end_date_tag.get_text(strip=True) if end_date_tag else None

    desc = tender.find("a", class_="description")
    title = desc.get_text(strip=True) if desc else None

    href = desc["href"] if desc and "href" in desc.attrs else ""
    region_part = href.split("/")[2] if href else None
    link = f"https://rostender.info/region/{region_part}/{number}" if region_part and number else None

    price = tender.find("div", class_="starting-price--price")
    price = price.get_text(strip=True) if price else None

    region = tender.find("div", class_="tender-address")
    region = region.get_text(strip=True) if region else None

    # создаем объект TenderModel
    try:
        model = TenderModel(
            number=number,
            start_date=start_date,
            end_date=end_date,
            title=title,
            url=link,
            region=region,
            price=price
        )
        clean_page.append(model)
    except Exception as e:
        print(f"Ошибка валидации модели TenderModel: {e}")


# Функция для парсинга одной страницы
async def parse_page(client: httpx.AsyncClient, page_url: str):
    try:
        # делаем запрос
        response = await client.get(page_url, timeout=10.0)
        response.raise_for_status()
        # парсим страницу
        soup = bs(response.text, "html.parser")
        tenders = soup.find_all("article", class_="tender-row row")
        clean_page = []
        for tender in tenders:
            parse_tender(tender, clean_page)
        return clean_page
    except Exception as e:
        print(f"Ошибка при обработке страницы {page_url}:\n{repr(e)}")
        traceback.print_exc()
        return []


# CLI-команда для извлечения и сохранения данных
@extractor_app.command("extract")
def extract(max: int = 10, output: str = "tenders.db"):
    asyncio.run(async_extract(max, output))


# функция для асинхронного извлечения и сохранения данных
async def async_extract(max: int, output: str):
    ext = os.path.splitext(output)[1].lower()
    output_dir = "data"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, output)

    # вычисляем количество страниц, которое нужно спарсить
    total_pages = ceil(max / 20)
    urls = [re.sub(r'page=\d+', f'page={i + 1}', parse_url) for i in range(total_pages)]

    # создаем список, в который будут добавляться спарсенные данные
    all_data = []
    # создаем клиент для асинхронных запросов
    async with httpx.AsyncClient() as client:
        # создаем список задач для парсинга страниц
        tasks = [parse_page(client, url) for url in urls]
        # парсим страницы
        results = await asyncio.gather(*tasks)
        for page_data in results:
            all_data.extend(page_data)

    # если output - файл БД, то сохраняем данные в БД
    if ext == ".db":
        await save_to_db(all_data, output_path)
        print(f"Данные сохранены в БД: {output_path}")
    # если output - файл CSV, то сохраняем данные в CSV
    elif ext == ".csv":
        with open(output_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=list(TenderModel.model_fields.keys()))
            writer.writeheader()
            for item in all_data:
                writer.writerow(item.dict())
        print(f"Данные сохранены в CSV: {output_path}")
    else:
        print("Неизвестный формат файла. Используйте .db или .csv")

