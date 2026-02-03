import typer
from pathlib import Path

exterminator_app = typer.Typer()
BASE_DIR = Path("data")  # корневая директория для работы с файлами

@exterminator_app.command()
def delete(
    path: Path = typer.Option(None, help="Имя файла для удаления (в папке data)."),
    all: bool = typer.Option(False, "--all", help="Удалить все .db и .csv файлы в папке data.")
):
    # Создаем папку data, если её нет
    BASE_DIR.mkdir(exist_ok=True)

    if all:
        for ext in ("*.db", "*.csv"):
            for file in BASE_DIR.glob(ext):
                if file.is_file():
                    try:
                        file.unlink()
                        print(f"Файл {file} успешно удалён")
                    except Exception as e:
                        typer.echo(f"Не удалось удалить {file}: {e}")

    elif path:
        file_path = BASE_DIR / path.name

        if file_path.exists():
            try:
                file_path.unlink()
                typer.echo(f"Файл {file_path} удалён.")
            except Exception as e:
                typer.echo(f"Ошибка при удалении: {e}")
        else:
            typer.echo(f"Файл {file_path} не найден.")

    else:
        typer.echo("Укажите --path для удаления конкретного файла (относительно папки data) или --all для массового удаления.")
