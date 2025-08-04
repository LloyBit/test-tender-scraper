# test-tender-scraper

## Настройка окружения

```bash

```

## Команды

### Создание и наполнение файла .csv/.db

Пример создания и наполнения файла с именем new_tenders 20-ю тендерами

```bash
python main.py extract --max 20 --output new_tenders.db
```

### Вывод файла .csv/.db

Пример вывода всех тендеров из файла new_tenders.db

```bash
python main.py show --output new_tenders.db
```

### Удаление файла .csv/.db или всех таких файлов в директории проекта

Пример удаления csv файла с именем new_tenders.db

```bash
python main.py delete --path new_tenders.db
```

Пример удаления всех файлов .csv и .db

```bash
python main.py delete --all 
```

### Запуск сервера раздачи json

```bash
python main.py host 
```

## Главное

Скрипт парсит сайт [rostender](https://rostender.info/extsearch)

## TODO

end-date теряется
сделать апишники
добавить создание csv