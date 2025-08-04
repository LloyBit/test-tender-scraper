from tabulate import tabulate
from ..database import get_connection
import typer

representer_app = typer.Typer()

MAX_TITLE_LEN = 20  # максимально допустимая длина для столбца title

def truncate(text, max_len=MAX_TITLE_LEN):
    if not isinstance(text, str):
        return text
    return text if len(text) <= max_len else text[:max_len-3] + "..."

# Вывод таблицы
@representer_app.command("show")
def show_table(output: str = "tenders.db"):
    with get_connection(output) as conn:
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM tenders")
        rows = cursor.fetchall()

        columns = [description[0] for description in cursor.description]

        if rows:
            truncated_rows = []
            for row in rows:
                row = list(row)
                # Обрезаем столбец title
                row[3] = truncate(row[3])
                truncated_rows.append(row)

            print(tabulate(truncated_rows, headers=columns, tablefmt="grid"))
        else:
            print("Таблица пустая")


