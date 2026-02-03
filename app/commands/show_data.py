import asyncio
import csv
import os

import aiosqlite
import typer
from tabulate import tabulate

representer_app = typer.Typer()
MAX_ROW_LEN = 20


def _truncate(text: str | None, max_len: int = MAX_ROW_LEN) -> str | None:
    """Shorten long strings for table display."""
    if not isinstance(text, str):
        return text
    return text if len(text) <= max_len else text[: max_len - 3] + "..."


@representer_app.command("show")
def show(output: str = "tenders.db"):
    asyncio.run(show_table(output))
    
async def show_table(output: str = "tenders.db"):
    ext = os.path.splitext(output)[1].lower()
    input_dir = "data"
    input_path = os.path.join(input_dir, output)

    if ext == ".db":
        # Читаю из БД
        if not os.path.exists(input_path):
            print(f"Файл {input_path} не найден.")
            return

        async with aiosqlite.connect(input_path) as db:
            cursor = await db.execute("SELECT * FROM tenders")
            rows = await cursor.fetchall()
            columns = [description[0] for description in cursor.description]
            await cursor.close()

            if rows:
                # Обрезаю длинные столбцы
                truncated_rows = []
                for row in rows:
                    row = list(row)
                    row[3] = _truncate(row[3], MAX_ROW_LEN)
                    row[5] = _truncate(row[5], MAX_ROW_LEN)
                    truncated_rows.append(row)

                # Отображаю таблицу
                print(tabulate(truncated_rows, headers=columns, tablefmt="grid"))
            else:
                print("Таблица пустая")

    elif ext == ".csv":
        if not os.path.exists(input_path):
            print(f"Файл {input_path} не найден.")
            return

        # Чтение CSV остаётся синхронным
        with open(input_path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            if not rows:
                print("CSV файл пустой")
                return

            truncated_rows = []
            for row in rows:
                row_copy = dict(row)
                row_copy["title"] = _truncate(row_copy.get("title"), MAX_ROW_LEN)
                row_copy["region"] = _truncate(row_copy.get("region"), MAX_ROW_LEN)
                truncated_rows.append(row_copy)

            print(tabulate(truncated_rows, headers="keys", tablefmt="grid"))

    else:
        print("Неизвестный формат файла. Поддерживаются .db и .csv")

if __name__ == "__main__":
    import sys
    asyncio.run(show_table(sys.argv[1] if len(sys.argv) > 1 else "tenders.db"))

