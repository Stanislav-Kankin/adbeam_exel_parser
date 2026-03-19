# adbeam_excel_parser

Легкий локальный парсер-аудитор сайтов из Excel.

## Что умеет текущий шаг

- читает `.xlsx`
- находит колонку с сайтом
- показывает preview строк
- проходит сайты по очереди
- делает базовый HTTP обход
- извлекает простые ecom/direct сигналы
- ставит начальный статус:
  - `FIT_NOW`
  - `FIT_LATER`
  - `NOT_FIT`
  - `BROKEN`
  - `HACKED`
  - `NO_SITE`

Это еще не финальная версия классификации.
Сейчас это первый рабочий rule-based обход без Playwright и без экспорта результата обратно в Excel.

## Структура проекта

```text
adbeam_excel_parser/
├── main.py
├── requirements.txt
├── README.md
└── src/
    └── adbeam_excel_parser/
        ├── __init__.py
        ├── audit_runner.py
        ├── excel_reader.py
        ├── gui_app.py
        ├── models.py
        └── site_audit.py
```

## Требования

- Windows / Linux / macOS
- Python 3.12+

## Установка

### Windows PowerShell

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Если PowerShell блокирует активацию

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

Потом снова:

```powershell
.\.venv\Scripts\Activate.ps1
```

## Как запустить

### Вариант 1. Локальный интерфейс

```powershell
python main.py
```

Дальше:
- выбери Excel-файл
- нажми **Проверить Excel** или **Начать обход сайтов**

### Вариант 2. CLI — только чтение Excel

```powershell
python main.py --input "C:\Users\Пользователь\Downloads\Основной сегмент 2026-03-19 12-30.xlsx"
```

### Вариант 3. CLI — полный обход сайтов

```powershell
python main.py --input "C:\Users\Пользователь\Downloads\Основной сегмент 2026-03-19 12-30.xlsx" --audit
```

## Как сейчас работает классификация

Положительные сигналы:
- каталог
- корзина
- купить / оформить заказ
- цены
- доставка
- оплата
- consumer language

Негативные сигналы:
- оставить заявку
- запросить КП
- B2B / промышленный язык
- мусорные / hacked keywords

## Ограничения текущего шага

- обход пока только последовательный
- JS-сайты пока не обрабатываются fallback-движком
- rule-based логика еще будет калиброваться
- результат пока выводится в JSON, а не в итоговый Excel

## Следующий шаг

Следующим шагом логично сделать:
- экспорт результата в новый `.xlsx`
- отдельные колонки с признаками и статусом
- улучшение правил классификации
- fallback для сложных сайтов
