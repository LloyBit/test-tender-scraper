import typer
from pathlib import Path

exterminator_app = typer.Typer()

# Удаление конкретного файла или всех связанных
@exterminator_app.command()
def delete(path: Path = typer.Option(None, help="Путь к удаляемому файлу."),
           all: bool = typer.Option(False, "--all", help="Удалить все .db и .csv файлы в текущей директории.")):
    
    # Сценарий удаления всех связанных файлов
    if all:
        for ext in ("*.db", "*.csv"):
            for file in Path(".").glob(ext):
                if file.is_file():
                    try:
                        file.unlink()
                        print(f"Файл {file} успешно удалён")
                    except Exception as e:
                        typer.echo(f"Не удалось удалить {file}: {e}")
                        
    # Сценарий удаления конкретного файла
    elif path:
        # Проверка, что удаление происходит в рабочей директории
        try:
            path.resolve().relative_to(Path.cwd().resolve())
        except ValueError:
            typer.echo(f"Удаление файлов вне рабочей директории запрещено: {path}")
            return
        
        if path.exists():
            try:
                path.unlink()
                typer.echo(f"Файл {path} удалён.")
            except Exception as e:
                typer.echo(f"Ошибка при удалении: {e}")
        else:
            typer.echo(f"Файл {path} не найден.")
            
    # Сценарий неправильного вызова
    else:
        typer.echo("Укажите --path для удаления конкретного файла или --all для массового удаления.")
