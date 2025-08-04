import httpx
from bs4 import BeautifulSoup as bs
import re 
from math import ceil
from app.database import save_to_db
import typer
import os
import csv

extractor_app = typer.Typer()

# Путь к сайту
parse_url = "https://rostender.info/extsearch?page=1"

# Парсит тендер на ключевую инфу
def parse_tender(tender, clean_page):
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

    clean_page.append({
        "number": number,
        "start_date": start_date,
        "end_date": end_date,
        "title": title,
        "url": link,
        "region": region,
        "price": price
    })

# Парсит страницу на тендеры, на них вызывает parse_tender
def parse_page(page_url: str, file_name="tenders.db"):
    resource = httpx.get(page_url)
    soup = bs(resource.text, "html.parser")
    tenders = soup.find_all("article", class_="tender-row row")
    
    clean_page = []
    
    for tender in tenders:
        parse_tender(tender, clean_page)
    
    return clean_page
   
# Возвращает URL нужной page
def choose_page(resource: str, page: int):
    return re.sub(r'page=\d+', f'page={page}', resource)

# Точка входа для команды
@extractor_app.command("extract")
def extract(max: int = 10, output: str = "tenders.db"):
    ext = os.path.splitext(output)[1].lower()

    output_dir = "data"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, output)

    all_data = []
    for pages_num in range(ceil(max / 20)):
        page_url = re.sub(r'page=\d+', f'page={pages_num + 1}', parse_url)
        data = parse_page(page_url)
        all_data.extend(data)

    if ext == ".db":
        save_to_db(all_data, output_path)
        print(f"Данные сохранены в БД: {output_path}")
    elif ext == ".csv":
        with open(output_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["number", "start_date", "end_date", "title", "url", "region", "price"])
            writer.writeheader()
            writer.writerows(all_data)
        print(f"Данные сохранены в CSV: {output_path}")
    else:
        print("Неизвестный формат файла. Используйте .db или .csv")
