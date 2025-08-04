from tabulate import tabulate
from ..database import get_connection
import typer
import csv
import os

representer_app = typer.Typer()

MAX_TITLE_LEN = 20  # максимально допустимая длина для столбца title

# Обрезает текст до максимально допустимой длины
def truncate(text, max_len=MAX_TITLE_LEN):
    if not isinstance(text, str):
        return text
    return text if len(text) <= max_len else text[:max_len-3] + "..."

# Вывод таблицы
@representer_app.command("show")
def show_table(output: str = "tenders.db"):
    ext = os.path.splitext(output)[1].lower()
    input_dir = "data"
    input_path = os.path.join(input_dir, output)

    if ext == ".db":
        if not os.path.exists(input_path):
            print(f"Файл {input_path} не найден.")
            return

        with get_connection(input_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM tenders")
            rows = cursor.fetchall()
            columns = [description[0] for description in cursor.description]

            if rows:
                truncated_rows = []
                for row in rows:
                    row = list(row)
                    row[3] = truncate(row[3])
                    truncated_rows.append(row)

                print(tabulate(truncated_rows, headers=columns, tablefmt="grid"))
            else:
                print("Таблица пустая")

    elif ext == ".csv":
        if not os.path.exists(input_path):
            print(f"Файл {input_path} не найден.")
            return

        with open(input_path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            if not rows:
                print("CSV файл пустой")
                return

            truncated_rows = []
            for row in rows:
                row_copy = dict(row)
                row_copy["title"] = truncate(row_copy.get("title"))
                truncated_rows.append(row_copy)

            print(tabulate(truncated_rows, headers="keys", tablefmt="grid"))

    else:
        print("Неизвестный формат файла. Поддерживаются .db и .csv")
