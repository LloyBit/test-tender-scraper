import httpx
from bs4 import BeautifulSoup as bs
import re 
from math import ceil
from app.database import create_db, insert_in_db
import typer

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

    end_date = tender.find("span", class_="tender__date-end")
    end_date = end_date.get_text(strip=True).replace("Окончание (МСК) ", "") if end_date else None

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

# Парсит страницу на тендеры, а их на ключевую инфу. Вставляет итог в ДБ
def parse_page(page_url: str, db_name="tenders.db"):
    resource = httpx.get(page_url)
    soup = bs(resource.text, "html.parser")
    tenders = soup.find_all("article", class_="tender-row row")
    
    clean_page = []
    
    for tender in tenders:
        parse_tender(tender, clean_page)
    
    # Вставка данных (с защитой от дубликатов по id)
    for item in clean_page:
        insert_in_db(item, db_name)

# Возвращает URL нужной страницы
def choose_page(resource: str, page: int):
    return re.sub(r'page=\d+', f'page={page}', resource)

# Работа с CLI
@extractor_app.command("extract")
def extract(max: int = 10, output: str = "tenders.db"):
    create_db(output)
    for pages_num in range(ceil(max / 20)):
        page_url = choose_page(parse_url, pages_num + 1)
        parse_page(page_url, output)