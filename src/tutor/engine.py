import subprocess
import os
import re
import json

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
        return None

class LocalTutorEngine:
    def __init__(self):
        self.kb_path = os.path.join(os.path.dirname(__file__), '../../knowledge_base')
        self.kb = self._load_kb()
        print(f"✅ Локальный AI-Тьютор инициализирован.")
        print(f"📚 Загружено модулей: {len(self.kb)}")
        for module in self.kb:
            topics = len(module.get('topics', {}))
            print(f"   • Модуль {module['module_id']}: {module['module_name']} ({topics} тем)")

    def _load_kb(self):
        """Загружает все JSON-файлы из knowledge_base/."""
        modules = []
        if not os.path.exists(self.kb_path):
            print(f"⚠️ Папка {self.kb_path} не найдена")
            return modules
        for filename in sorted(os.listdir(self.kb_path)):
            if filename.endswith('.json'):
                filepath = os.path.join(self.kb_path, filename)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        modules.append(json.load(f))
                except Exception as e:
                    print(f"⚠️ Ошибка загрузки {filename}: {e}")
        return modules

    def _find_topic(self, query: str):
        """Ищет тему в базе знаний по ключевым словам."""
        query_lower = query.lower()
        for module in self.kb:
            for topic_key, topic_data in module.get('topics', {}).items():
                for keyword in topic_data.get('keywords', []):
                    if re.search(keyword, query_lower):
                        return topic_data, topic_key, module
        return None, None, None

    def explain(self, query: str) -> str:
        topic, key, module = self._find_topic(query)
        if not topic:
            return "🤔 Пока не знаю, как это объяснить. Попробуй спросить про: переменные, функции, условия, циклы, списки."
        explanations = topic.get('explanations', [])
        if not explanations:
            return "Для этой темы пока нет готовых объяснений."
        # Берём случайную аналогию (чтобы не повторяться)
        import random
        chosen = random.choice(explanations)
        return f"**{chosen['analogy']}**\n\n{chosen['text']}"

    def give_hint(self, query: str) -> str:
        topic, key, module = self._find_topic(query)
        if not topic:
            return "💡 Попробуй разбить задачу на мелкие шаги. С чего можно начать?"
        hints = topic.get('hints', [])
        if not hints:
            return "💡 Подсказок пока нет. Попробуй переформулировать вопрос."
        import random
        return f"💡 {random.choice(hints)}"

    def check_code(self, code: str, context_query: str = "") -> str:
        """Проверяет код по правилам из базы знаний."""
        topic, key, module = self._find_topic(context_query) if context_query else (None, None, None)
        
        checks = []
        if topic:
            checks = topic.get('code_checks', [])
        
        # Применяем все правила
        for rule in checks:
            if re.search(rule['pattern'], code, re.MULTILINE):
                return rule['error']
        
        # Базовая проверка синтаксиса (всегда активна)
        if ('def ' in code or 'if ' in code or 'for ' in code or 'while ' in code or 'else' in code):
            lines = code.split('\n')
            for i, line in enumerate(lines, 1):
                stripped = line.rstrip()
                if any(stripped.startswith(kw) for kw in ['def ', 'if ', 'elif ', 'else', 'for ', 'while ']):
                    if not stripped.endswith(':'):
                        return f"❌ Строка {i}: пропущено двоеточие ':' в конце."
        
        return "✅ Код выглядит корректно! (локальная проверка)"

    def ask(self, user_query: str, action: str = "explain", code: str = None) -> str:
        """Основной метод взаимодействия с тьютором."""
        if action == "explain":
            return self.explain(user_query)
        elif action == "hint":
            return self.give_hint(user_query)
        elif action == "check":
            return self.check_code(code or user_query, user_query)
        else:
            return "❓ Неизвестное действие. Используй: explain, hint, check."

if __name__ == "__main__":
    tutor = LocalTutorEngine()
    
    print("\n" + "="*50)
    print("ТЕСТ 1: Объяснение (функции)")
    print("="*50)
    print(tutor.ask("Как работают функции?", action="explain"))
    
    print("\n" + "="*50)
    print("ТЕСТ 2: Подсказка (переменные)")
    print("="*50)
    print(tutor.ask("Не могу разобраться с переменными", action="hint"))
    
    print("\n" + "="*50)
    print("ТЕСТ 3: Проверка кода с ошибкой")
    print("="*50)
    bad_code = "def hello()\n    print('hi')"
    print(f"Код:\n{bad_code}")
    print(f"\nРезультат: {tutor.ask('функции', action='check', code=bad_code)}")
    
    print("\n" + "="*50)
    print("ТЕСТ 4: Правильный код")
    print("="*50)
    good_code = "def hello():\n    print('hi')"
    print(f"Код:\n{good_code}")
    print(f"\nРезультат: {tutor.ask('функции', action='check', code=good_code)}")
