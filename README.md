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
- сохраняет новый `.xlsx`, не ломая исходный файл
- по возможности сохраняет исходную структуру листа и добавляет в начало служебные колонки
- красит строки: зеленый / желтый / красный

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
        ├── excel_exporter.py
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

## Как запустить

### Вариант 1. Локальный интерфейс

```powershell
python main.py
```

Дальше:
- выбери Excel-файл
- нажми **Проверить Excel** или **Начать обход и сохранить Excel**

После обхода рядом с исходным файлом появится новый файл:

```text
<имя_файла>_audited.xlsx
```

### Вариант 2. CLI — только чтение Excel

```powershell
python main.py --input "C:\Users\Пользователь\Downloads\Основной сегмент 2026-03-19 12-30.xlsx"
```

### Вариант 3. CLI — полный обход сайтов и сохранение нового Excel

```powershell
python main.py --input "C:\Users\Пользователь\Downloads\Основной сегмент 2026-03-19 12-30.xlsx" --audit
```

## Что добавляется в итоговый Excel

В начало листа добавляются колонки:
- `AdBeam статус`
- `AdBeam причина`
- `AdBeam HTTP`

Дополнительно строка подсвечивается:
- зеленый — `FIT_NOW`
- желтый — `FIT_LATER`
- красный — все негативные статусы

## Ограничения текущего шага

- обход пока только последовательный
- JS-сайты пока не обрабатываются fallback-движком
- rule-based логика еще будет калиброваться
- окраска строки может перекрывать редкие исходные заливки, если они были в исходном Excel

## Следующий шаг

Следующим шагом логично сделать:
- отдельные служебные колонки с URL/title/domain
- улучшение правил классификации
- fallback для сложных сайтов
- пакетную обработку нескольких файлов
