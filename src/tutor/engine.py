import subprocess
import os
import re

def get_secret(path: str) -> str:
    """Безопасно получает секрет из GPG-хранилища pass (для крайних случаев)."""
    try:
        result = subprocess.run(
            ['pass', 'show', path], 
            capture_output=True, 
            text=True, 
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        return None  # Возвращаем None, если секрета нет (LLM не используется)

class LocalTutorEngine:
    def __init__(self):
        self.kb_path = os.path.join(os.path.dirname(__file__), '../../knowledge_base')
        self.llm_enabled = False  # По умолчанию LLM отключен для оффлайн-работы
        
        # Загружаем локальную базу знаний (заглушка, в будущем будет парсинг JSON/SQLite)
        self.kb = self._load_local_kb()
        print("✅ Локальный AI-Тьютор инициализирован. LLM отключен. Работаем оффлайн.")

    def _load_local_kb(self):
        """Загружает предзаготовленные ответы из базы знаний."""
        return {
            "функции": {
                "explanation": "Функция — это как блендер 🥤. Кидаешь яблоки (аргументы), жмёшь кнопку — получаешь сок (результат).",
                "hint": "Подумай: что функция должна принимать на вход и что возвращать через return?",
                "code_check": "Проверь, есть ли двоеточие ':' после объявления def и правильный ли отступ."
            },
            "переменные": {
                "explanation": "Переменная — это коробка с наклейкой (именем), внутри которой лежит значение.",
                "hint": "Убедись, что имя переменной не начинается с цифры и не содержит пробелов.",
                "code_check": "Проверь, не используешь ли ты зарезервированные слова Python (например, 'if', 'for') как имена переменных."
            },
            "default": {
                "explanation": "Я пока учусь. Попробуй спросить про 'функции' или 'переменные', чтобы увидеть, как это работает.",
                "hint": "Попробуй разбить задачу на более мелкие шаги или переформулировать вопрос.",
                "code_check": "Код выглядит нормально, но я пока могу проверять только базовый синтаксис."
            }
        }

    def _find_best_match(self, query: str) -> str:
        """Простой поиск по ключевым словам в локальной базе знаний."""
        query_lower = query.lower()
        for keyword in self.kb.keys():
            if keyword in query_lower:
                return keyword
        return "default"

    def explain(self, query: str) -> str:
        keyword = self._find_best_match(query)
        return self.kb[keyword]["explanation"]

    def give_hint(self, query: str) -> str:
        keyword = self._find_best_match(query)
        return self.kb[keyword]["hint"]

    def check_code(self, code: str) -> str:
        """Локальная статическая проверка кода без LLM (через regex)."""
        if "def " in code and ":" not in code:
            return "❌ Ошибка: после объявления функции (def) обязательно нужно двоеточие ':'."
        if "for " in code and ":" not in code:
            return "❌ Ошибка: после оператора цикла (for) обязательно нужно двоеточие ':'."
        if "if " in code and ":" not in code:
            return "❌ Ошибка: после условия (if) обязательно нужно двоеточие ':'."
        return "✅ Код выглядит синтаксически корректным! (Локальная проверка)"

    def ask(self, user_query: str, action: str = "explain") -> str:
        """Основной метод взаимодействия. Работает полностью оффлайн."""
        if action == "explain":
            return self.explain(user_query)
        elif action == "hint":
            return self.give_hint(user_query)
        elif action == "check":
            return self.check_code(user_query)
        else:
            return "Неизвестное действие. Используй: explain, hint, check."

if __name__ == "__main__":
    tutor = LocalTutorEngine()
    print("\n--- Тест объяснения ---")
    print(tutor.ask("Как работают функции?", action="explain"))
    print("\n--- Тест проверки кода ---")
    print(tutor.ask("def hello()", action="check"))
