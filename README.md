# adbeam_excel_parser

Минимальный стартовый каркас проекта для аудита сайтов из Excel.

## Что умеет текущий шаг

- читает `.xlsx`
- берет первый лист
- читает заголовки
- пытается найти колонку с сайтом
- считает строки с сайтами
- выводит JSON summary в консоль
- открывает простое локальное окно для выбора Excel-файла кнопкой

Это еще не парсер сайтов.
Сейчас это безопасный стартовый каркас для чтения Excel и удобного локального запуска.

## Структура проекта

```text
adbeam_excel_parser/
├── main.py
├── requirements.txt
├── README.md
└── src/
    └── adbeam_excel_parser/
        ├── __init__.py
        ├── excel_reader.py
        ├── gui_app.py
        └── models.py
```

## Требования

- Windows / Linux / macOS
- Python 3.12+

## Как создать виртуальное окружение в Windows PowerShell

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Если PowerShell блокирует активацию

Открой PowerShell **от имени пользователя** и выполни:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

Потом снова:

```powershell
.\.venv\Scripts\Activate.ps1
```

## Как запустить

### Вариант 1. Простой локальный интерфейс

```powershell
python main.py
```

Откроется окно, где можно:
- выбрать Excel-файл кнопкой
- запустить проверку
- увидеть JSON summary прямо в окне

### Вариант 2. Старый CLI-режим

```powershell
python main.py --input "C:\Users\Пользователь\Downloads\Основной сегмент 2026-03-19 12-30.xlsx"
```

## Что будет на выходе

В окне или в консоли появится JSON примерно такого вида:

```json
{
  "file_path": "C:\\dev\\prod\\adbeam_excel_parser\\data\\companies.xlsx",
  "sheet_name": "Sheet1",
  "total_rows": 100,
  "headers": ["Компания", "Сайт"],
  "website_columns": ["Сайт"],
  "rows_with_websites": 87,
  "preview": []
}
```

## Что уже проверено

На текущем этапе мы подтвердили:
- проект запускается локально
- Excel читается
- колонка с сайтами находится
- preview строк строится корректно

## Следующий шаг

Следующим шагом логично добавить:
- нормализацию URL
- базовый HTTP обход сайтов
- первичную feature extraction логику
- первые rule-based статусы
