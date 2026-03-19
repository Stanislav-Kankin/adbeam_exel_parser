# adbeam_excel_parser

Минимальный стартовый каркас проекта для аудита сайтов из Excel.

## Что умеет текущий шаг

- читает `.xlsx`
- берет первый лист
- читает заголовки
- пытается найти колонку с сайтом
- считает строки с сайтами
- выводит JSON summary в консоль

Это еще не парсер сайтов.
Сейчас это только безопасный стартовый каркас для чтения Excel.

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
        └── models.py
```

## Требования

- Windows / Linux / macOS
- Python 3.12+

## Как создать виртуальное окружение в Windows PowerShell

### Вариант 1. Через `py`

```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### Вариант 2. Через `python`, если он есть в PATH

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
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

```powershell
python main.py --input .\data\companies.xlsx
```

## Что будет на выходе

В консоли появится JSON примерно такого вида:

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

## Следующий шаг

Следующим шагом можно добавить:

- нормализацию URL
- базовый HTTP обход сайтов
- первичную feature extraction логику
- первые rule-based статусы
