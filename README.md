# test-tender-scraper

Парсинг тендеров с [rostender.info](https://rostender.info/extsearch): сохранение в .db/.csv и API для отдачи JSON.

## Установка

```bash
pip install uv
uv sync
```

(venv создаётся и активируется через `uv venv` при необходимости.)

## Команды

Все команды через `uv run python -m app.main <команда> ...`.

| Действие | Пример |
|----------|--------|
| Спарсить и сохранить | `uv run python -m app.main extract --max 20 --output new_tenders.db` |
| Показать данные из файла | `uv run python -m app.main show --output new_tenders.db` |
| Удалить файл в `data/` | `uv run python -m app.main delete --path new_tenders.db` |
| Удалить все .db и .csv в `data/` | `uv run python -m app.main delete --all` |
| Запустить API | `uv run python -m app.main host` |

Файлы создаются в папке `data/`. Поддерживаются форматы `.db` (SQLite) и `.csv`.

## API

После `host` доступен эндпоинт `GET /tenders/?max_items=10` — возвращает JSON со списком тендеров (парсинг на лету, без записи во временные файлы).

Пример клиента: `app/client.py` — запрос к локальному API и вывод JSON.

## Структура

- `app/parser.py` — разбор HTML (RostenderParser).
- `app/scraper.py` — загрузка страниц и сбор тендеров (RostenderScraper).
- `app/database.py` — работа с SQLite (таблица tenders).
- `app/commands/` — CLI: extract, show, delete, host.
- `app/api/tenders.py` — FastAPI роут `/tenders`.
