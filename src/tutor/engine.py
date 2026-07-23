import subprocess
import json
import os

def get_secret(path: str) -> str:
    """Безопасно получает секрет из GPG-хранилища pass."""
    try:
        result = subprocess.run(
            ['pass', 'show', path], 
            capture_output=True, 
            text=True, 
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        raise ValueError(f"Не удалось получить секрет: {path}. Убедитесь, что он добавлен через 'pass insert'.")

class AITutorEngine:
    def __init__(self):
        # Читаем API ключ безопасно, без хардкода
        self.api_key = get_secret('llm/api_key')
        self.kb_path = os.path.join(os.path.dirname(__file__), '../../knowledge_base')
        print(f"✅ Ядро тьютора инициализировано. База знаний: {self.kb_path}")

    def get_context(self, module_id: int, topic: str) -> str:
        """Заглушка для получения контекста из базы знаний."""
        # В будущем здесь будет парсинг Markdown-файлов из knowledge_base/
        return f"Контекст для модуля {module_id}, тема: {topic}. (База знаний в разработке)"

    def ask(self, user_query: str, module_id: int, topic: str) -> str:
        """Основной метод взаимодействия с тьютором."""
        context = self.get_context(module_id, topic)
        # Здесь будет логика вызова LLM с системным промптом и контекстом
        return f"🤖 Тьютор получил вопрос: '{user_query}' в контексте: {context}"

if __name__ == "__main__":
    tutor = AITutorEngine()
    response = tutor.ask("Объясни функции в Python", module_id=1, topic="Основы Python")
    print(response)
