from contextlib import contextmanager
import sqlite3

import re

# Контекстный менеджер для работы с соединением
@contextmanager
def get_connection(db_name="tenders.db"):
    conn = sqlite3.connect(db_name)
    try:
        yield conn
    finally:
        conn.commit()
        conn.close()


# Создать файл ДБ если еще не создан
def create_db(db_name="tenders.db"):
    with get_connection(db_name) as conn:
        cursor = conn.cursor()
        cursor.execute("""
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


# Очистка текста от ненужных символов
def clean(text):
    if not isinstance(text, str):
        return text
    text = re.sub(r'\s+', ' ', text)
    return text.strip()
    
# Вставка записи в БД
def insert_in_db(item, db_name="tenders.db"):
    with get_connection(db_name) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT OR IGNORE INTO tenders (number, start_date, end_date, title, url, region, price)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            clean(item['number']),
            clean(item['start_date']),
            clean(item['end_date']),
            clean(item['title']),
            clean(item['url']),
            clean(item['region']),
            clean(item['price'])
        ))
        
# Сохранение данных в ДБ 
def save_to_db(data, db_name="tenders.db"):
    create_db(db_name)
    for item in data:
        insert_in_db(item, db_name)  


