import httpx
import json

BASE_URL = "http://127.0.0.1:8000"  # Адрес запуска FastAPI

def fetch_tenders(max_items=10):
    try:
        response = httpx.get(f"{BASE_URL}/tenders/", params={"max_items": max_items})
        response.raise_for_status()
        tenders = response.json()

        if not tenders:
            print("Нет доступных тендеров.")
            return

        # Печатаем первый объект в формате JSON с отступами
        print("Первый тендер в формате JSON:\n")
        print(json.dumps(tenders[0], indent=4, ensure_ascii=False))

    except httpx.RequestError as e:
        print(f"Ошибка запроса: {e}")
    except httpx.HTTPStatusError as e:
        print(f"Ошибка статуса: {e.response.status_code} — {e.response.text}")

if __name__ == "__main__":
    fetch_tenders(max_items=5)