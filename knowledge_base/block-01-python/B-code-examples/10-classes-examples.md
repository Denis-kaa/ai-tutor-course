---
block_id: 1
section: "B"
topic: "Примеры: классы и ООП"
word_count: 1800
difficulty: "beginner"
tags: ["python", "examples", "classes", "oop", "init", "self"]
created: "2026-07-24"
---

# Примеры кода: Классы и ООП

## Пример 1: Базовый класс с __init__

**Задача:** Создать класс и несколько объектов.

```python
# Определяем класс Dog (чертёж собаки)
class Dog:
    # __init__ — конструктор, вызывается при создании объекта
    def __init__(self, name, breed):   # self — сам создаваемый объект
        self.name = name               # Сохраняем имя как атрибут объекта
        self.breed = breed             # Сохраняем породу как атрибут
        self.energy = 100              # Энергия по умолчанию = 100

# Создаём ОБЪЕКТЫ по чертежу Dog
dog1 = Dog("Шарик", "Дворняжка")   # self.name="Шарик", self.breed="Дворняжка"
dog2 = Dog("Рекс", "Овчарка")      # Другой объект с другими данными

# Читаем атрибуты через точку
print(dog1.name)                # Шарик
print(dog2.breed)               # Овчарка
print(dog1.energy)              # 100 (у обоих по умолчанию)
```

**Разбор:**
`class Имя:` объявляет чертёж. `__init__` выполняется автоматически при `Dog(...)`. `self` — ссылка на конкретный объект, через него сохраняются атрибуты (`self.name`). Каждый объект хранит свои данные независимо.

---

## Пример 2: Методы и self

**Задача:** Добавить объекту поведение (методы).

```python
class BankAccount:
    def __init__(self, owner, balance=0):   # balance по умолчанию 0
        self.owner = owner                  # Владелец счёта
        self.balance = balance              # Текущий баланс

    # Метод — функция внутри класса, первый параметр self
    def deposit(self, amount):              # Внести деньги
        self.balance += amount              # Увеличиваем баланс объекта
        return f"Внесено {amount}. Баланс: {self.balance}"

    def withdraw(self, amount):             # Снять деньги
        if amount > self.balance:           # Проверка: хватает ли денег
            return "Недостаточно средств!"  # Возвращаем ошибку строкой
        self.balance -= amount              # Уменьшаем баланс
        return f"Снято {amount}. Баланс: {self.balance}"

    def info(self):                         # Показать информацию
        return f"{self.owner}: {self.balance} руб."

# Создаём объект и вызываем методы
acc = BankAccount("Иван", 1000)   # Баланс 1000
print(acc.deposit(500))           # Внесено 500. Баланс: 1500
print(acc.withdraw(200))          # Снято 200. Баланс: 1300
print(acc.withdraw(9999))         # Недостаточно средств!
print(acc.info())                 # Иван: 1300 руб.
```

**Разбор:**
Метод — функция, привязанная к объекту, всегда с `self` первым параметром. Через `self` метод читает и меняет атрибуты именно ЭТОГО объекта. При вызове `acc.deposit(500)` Python сам подставляет `acc` в `self`, поэтому передаём только `500`.

---

## Пример 3: Наследование и super()

**Задача:** Создать дочерний класс, расширяющий родительский.

```python
# Родительский класс
class Employee:
    def __init__(self, name, salary):
        self.name = name              # Имя сотрудника
        self.salary = salary          # Зарплата

    def describe(self):               # Описание сотрудника
        return f"{self.name}, зарплата {self.salary}"

# Дочерний класс — наследует от Employee
class Manager(Employee):
    def __init__(self, name, salary, team_size):
        super().__init__(name, salary)   # Вызываем __init__ родителя!
        self.team_size = team_size       # Своё поле — размер команды

    # Переопределяем метод родителя (override)
    def describe(self):
        base = super().describe()        # Берём описание от родителя
        return f"{base}, команда {self.team_size} чел."

    # Новый метод, которого нет у родителя
    def give_bonus(self, amount):
        self.salary += amount
        return f"Бонус {amount} выдан {self.name}"

m = Manager("Ольга", 150000, 5)   # Создаём менеджера
print(m.describe())               # Ольга, зарплата 150000, команда 5 чел.
print(m.give_bonus(20000))        # Бонус 20000 выдан Ольга
print(m.name)                     # Ольга (унаследовано от Employee)
```

**Разбор:**
`class Child(Parent):` наследует всё от родителя. `super().__init__(...)` вызывает конструктор родителя, чтобы не дублировать код инициализации общих полей. Переопределённый метод заменяет родительский; через `super().method()` можно обратиться к оригиналу.

---

## Пример 4: Магические методы __str__ и __repr__

**Задача:** Сделать красивый вывод объекта через print.

```python
class Point:
    def __init__(self, x, y):
        self.x = x                  # Координата X
        self.y = y                  # Координата Y

    # __str__ — что видит пользователь при print()
    def __str__(self):
        return f"Точка({self.x}, {self.y})"

    # __repr__ — что видит разработчик (для отладки)
    def __repr__(self):
        return f"Point(x={self.x}, y={self.y})"

    # __eq__ — как сравнивать объекты через ==
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

p = Point(3, 4)
print(p)                        # Точка(3, 4)  — сработал __str__
print(repr(p))                  # Point(x=3, y=4)  — сработал __repr__

p2 = Point(3, 4)
print(p == p2)                  # True — сработал __eq__
# Без __eq__ было бы False (разные объекты в памяти)
```

**Разбор:**
Магические методы (dunder, с двойным подчёркиванием) перегружают поведение операторов. `__str__` для `print`, `__repr__` для отладки, `__eq__` для `==`, `__len__` для `len()`, `__add__` для `+`. Без них объекты сравниваются по адресу в памяти и печатаются как `<__main__.Point object at 0x...>`.

---

## Пример 5: Атрибуты класса vs атрибуты объекта (ЛОВУШКА)

**Задача:** Показать опасную ловушку с изменяемыми атрибутами класса.

```python
# ❌ НЕПРАВИЛЬНО: список как атрибут класса — ОДИН на всех!
class BadTeam:
    members = []                  # Это атрибут КЛАССА, общий для всех объектов!

    def add(self, name):
        self.members.append(name)   # self.members указывает на общий список

team_a = BadTeam()
team_a.add("Иван")
team_b = BadTeam()                # Создали ДРУГОЙ объект
team_b.add("Мария")

print(team_a.members)             # ['Иван', 'Мария'] — УПС! Иван попал в team_b!
print(team_b.members)             # ['Иван', 'Мария'] — общий список!

print("---")

# ✅ ПРАВИЛЬНО: создаём список в __init__ — у каждого объекта свой
class GoodTeam:
    def __init__(self):
        self.members = []         # СВОЙ список для КАЖДОГО объекта

    def add(self, name):
        self.members.append(name)

team_x = GoodTeam()
team_x.add("Иван")
team_y = GoodTeam()
team_y.add("Мария")

print(team_x.members)             # ['Иван'] — только свои
print(team_y.members)             # ['Мария'] — только свои
```

**Разбор:**
Атрибуты, объявленные прямо в теле класса (вне `__init__`), принадлежат КЛАССУ и делятся между всеми объектами. Если это изменяемый объект (список, словарь) — изменения увидят все. Правило: изменяемые атрибуты создавай в `__init__` через `self.имя = []`.

---

## Пример 6: Проверка типов — isinstance и type

**Задача:** Проверить, к какому классу принадлежит объект.

```python
class Animal:
    pass                        # Пустой класс-родитель

class Dog(Animal):
    pass                        # Dog наследует от Animal

class Cat(Animal):
    pass                        # Cat наследует от Animal

rex = Dog()                     # Создаём собаку

# isinstance — проверяет принадлежность классу И его потомкам
print(isinstance(rex, Dog))     # True (rex — это Dog)
print(isinstance(rex, Animal))  # True (Dog — потомок Animal!)
print(isinstance(rex, Cat))     # False (rex не кот)

# issubclass — проверяет наследование между классами
print(issubclass(Dog, Animal))  # True (Dog наследует от Animal)
print(issubclass(Cat, Dog))     # False

# type — ТОЧНЫЙ класс объекта (без учёта наследования)
print(type(rex) == Dog)         # True
print(type(rex) == Animal)      # False (точный класс — Dog, не Animal)
```

**Разбор:**
`isinstance` учитывает наследование — предпочтительный способ проверки типа. `type() ==` проверяет ТОЧНЫЙ класс без потомков — используй редко. `issubclass` работает с классами, а не объектами. В реальном коде чаще полагаются на "утиную типизацию" (важно поведение, а не класс), но проверки нужны для валидации.

---

## Частые ошибки новичков

| Ошибка | Пример | Решение |
|--------|--------|---------|
| Забыл self | `def __init__(name):` | `def __init__(self, name):` |
| Изменяемый атрибут класса | `members = []` в теле | Создавай в `__init__` |
| Вызов без () | `print(Dog)` вместо `Dog()` | Скобки создают объект |
| Забыл super().__init__ | поля родителя не заданы | Вызывай `super().__init__(...)` |
| Обращение без self | `return name` в методе | `return self.name` |
