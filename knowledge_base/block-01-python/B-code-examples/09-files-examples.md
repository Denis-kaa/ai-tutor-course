---
block_id: 1
section: "B"
topic: "Примеры: работа с файлами"
word_count: 1800
difficulty: "beginner"
tags: ["python", "examples", "files", "io", "json", "csv"]
created: "2026-07-24"
---

# Примеры кода: Работа с файлами

## Пример 1: Запись и чтение текста через with

**Задача:** Сохранить текст в файл и прочитать его обратно.

```python
# Запись в файл (режим "w" — создаёт файл или ПЕРЕЗАПИСЫВАЕТ)
with open("notes.txt", "w", encoding="utf-8") as f:   # Открываем для записи
    f.write("Первая строка\n")    # \n — перенос строки
    f.write("Вторая строка\n")    # write не добавляет \n сам!
# Блок with закрылся — файл автоматически сохранился и закрылся

# Чтение всего файла сразу (режим "r" — чтение)
with open("notes.txt", "r", encoding="utf-8") as f:   # Открываем для чтения
    content = f.read()          # Читаем ВЕСЬ файл в одну строку
print(content)
# Первая строка
# Вторая строка
```

**Разбор:**
`with open(...) as f` — контекстный менеджер, гарантирующий закрытие файла даже при ошибке. `encoding="utf-8"` обязательно для кириллицы. Режим `"w"` перезаписывает файл с нуля. `write` не добавляет перенос строки — ставь `\n` сам.

---

## Пример 2: Режимы w, a, r и чтение построчно

**Задача:** Дописать в файл и читать построчно.

```python
# Режим "a" (append) — ДОПИСЫВАЕТ в конец, не стирая старое
with open("log.txt", "a", encoding="utf-8") as f:
    f.write("Событие 1\n")      # Добавится в конец
    f.write("Событие 2\n")      # Добавится следом

# Ещё раз дописываем — старые строки остались!
with open("log.txt", "a", encoding="utf-8") as f:
    f.write("Событие 3\n")

print("--- Чтение построчно ---")

# Чтение построчно — экономит память на больших файлах
with open("log.txt", "r", encoding="utf-8") as f:
    for line in f:              # f сам итерируется по строкам!
        print(line.strip())     # strip() убирает \n в конце
# Событие 1 / Событие 2 / Событие 3

print("--- readlines ---")

# readlines() — все строки списком
with open("log.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()       # ['Событие 1\n', 'Событие 2\n', 'Событие 3\n']
print(len(lines))               # 3
```

**Разбор:**
`"a"` дописывает, `"w"` стирает и пишет заново — не перепутай! Перебор `for line in f` читает по одной строке, не загружая весь файл в память — это правильно для больших файлов. `readlines()` даёт список всех строк (с `\n` на концах).

---

## Пример 3: JSON — сохранение и загрузка данных

**Задача:** Сохранить словарь в файл и загрузить обратно.

```python
import json                   # Встроенный модуль для работы с JSON

# Данные для сохранения (словарь со списком внутри)
user = {
    "name": "Алексей",
    "age": 30,
    "skills": ["Python", "SQL", "Git"]
}

# Сохранение словаря в JSON-файл (json.dump — в файл)
with open("user.json", "w", encoding="utf-8") as f:
    json.dump(user, f, ensure_ascii=False, indent=2)
    # ensure_ascii=False — кириллица как есть, а не \u0410
    # indent=2 — красивый отступ в 2 пробела

# Загрузка из JSON-файла (json.load — из файла)
with open("user.json", "r", encoding="utf-8") as f:
    loaded = json.load(f)       # Читаем и парсим в словарь

print(loaded["name"])           # Алексей
print(loaded["skills"][0])      # Python

# json.dumps / json.loads — работа со СТРОКОЙ (не файлом)
text = json.dumps(user, ensure_ascii=False)   # Словарь -> строка JSON
print(text)                     # {"name": "Алексей", ...}
back = json.loads(text)         # Строка JSON -> словарь
print(back["age"])              # 30
```

**Разбор:**
`dump`/`load` работают с файлом, `dumps`/`loads` — со строкой (s = string). `ensure_ascii=False` сохраняет кириллицу читаемой. `indent` делает JSON красивым. JSON поддерживает словари, списки, строки, числа, bool, null — но НЕ кортежи и множества.

---

## Пример 4: CSV — табличные данные

**Задача:** Записать и прочитать таблицу в формате CSV.

```python
import csv                    # Встроенный модуль для CSV

# Данные — список строк (каждая строка — список значений)
rows = [
    ["Имя", "Возраст", "Город"],     # Заголовок
    ["Аня", "25", "Москва"],
    ["Боря", "30", "Казань"],
    ["Вера", "28", "Сочи"]
]

# Запись в CSV (newline="" ВАЖНО на Windows/Termux)
with open("users.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)          # Создаём объект-писатель
    writer.writerows(rows)          # writerows — записать все строки сразу

print("--- Чтение CSV ---")

# Чтение из CSV
with open("users.csv", "r", encoding="utf-8") as f:
    reader = csv.reader(f)          # Создаём объект-читатель
    for row in reader:              # row — список значений строки
        print(row)
# ['Имя', 'Возраст', 'Город'] / ['Аня', '25', 'Москва'] / ...

print("--- Чтение как словарей ---")

# DictReader — каждая строка как словарь с заголовками-ключами
with open("users.csv", "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)      # Заголовок станет ключами
    for row in reader:
        print(f"{row['Имя']} из {row['Город']}")
# Аня из Москвы / Боря из Казани / Вера из Сочи
```

**Разбор:**
CSV — простой табличный формат. `newline=""` в `open` при записи предотвращает лишние пустые строки. `writerows` пишет список строк за раз. `DictReader` удобен, когда нужно обращаться к колонкам по имени, а не по индексу.

---

## Пример 5: Проверки через os.path

**Задача:** Проверить существование файла перед открытием.

```python
import os                     # Модуль для работы с ОС и путями

filename = "notes.txt"        # Имя файла для проверки

# exists — существует ли файл или папка
if os.path.exists(filename):
    print(f"Файл {filename} найден")
else:
    print(f"Файл {filename} НЕ найден — создаём")
    with open(filename, "w", encoding="utf-8") as f:
        f.write("Создан автоматически\n")

# isfile / isdir — файл это или папка
print(os.path.isfile(filename))   # True (это файл)
print(os.path.isdir(filename))    # False (это не папка)

# getsize — размер файла в байтах
print("Размер:", os.path.getsize(filename), "байт")

# listdir — список файлов в папке
print("Файлы в текущей папке:")
for name in os.listdir("."):      # "." — текущая папка
    print(" -", name)
```

**Разбор:**
`os.path.exists` защищает от `FileNotFoundError`. `isfile`/`isdir` различают файл и папку. `getsize` даёт размер в байтах. `listdir(".")` перечисляет содержимое текущей директории. Для более современного API смотри `pathlib.Path` (в разделе A, тема 13).

---

## Пример 6: Обработка ошибок при работе с файлами

**Задача:** Не падать, если файл недоступен.

```python
filename = "maybe_exists.txt"   # Файла может не быть

# Безопасное чтение с обработкой всех типичных ошибок
try:
    with open(filename, "r", encoding="utf-8") as f:
        data = f.read()
    print("Прочитано:", data)
except FileNotFoundError:       # Файл не найден
    print(f"Файл {filename} не существует")
except PermissionError:         # Нет прав на чтение
    print(f"Нет прав читать {filename}")
except UnicodeDecodeError:      # Не та кодировка
    print("Ошибка кодировки — попробуй другой encoding")
except Exception as e:          # Любая другая ошибка
    print(f"Неизвестная ошибка: {e}")
```

**Разбор:**
При работе с файлами лови конкретные исключения: `FileNotFoundError` (нет файла), `PermissionError` (нет прав), `UnicodeDecodeError` (не та кодировка). Контекстный менеджер `with` закрывает файл даже если внутри `try` случилась ошибка — поэтому `finally` с `f.close()` не нужен.

---

## Частые ошибки новичков

| Ошибка | Пример | Решение |
|--------|--------|---------|
| Забыл encoding | кириллица ломается | Всегда `encoding="utf-8"` |
| "w" стёр данные | потерял старое | Для дозаписи используй `"a"` |
| Забыл \n в write | всё в одну строку | Добавляй `"\n"` вручную |
| Не закрыл файл | `f = open(...)` без close | Используй `with` |
| FileNotFoundError | открыл несуществующий | Проверь `os.path.exists` или `try/except` |
