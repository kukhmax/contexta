import random
from typing import List, Dict, Any
from app.models.schemas import StoryRequest

class RuleBasedGenerator:
    """
    Шаг 1: Правила и шаблоны (Без ИИ).
    Определяет, КАКИЕ слова и грамматику мы хотим видеть в истории.
    """

    # База знаний (в будущем - БД)
    # Формат: 'word': {'base': '...', 'A1': '...', 'A2': '...'}
    VOCAB_DB = {
        "daily life": ["wake up", "breakfast", "bus", "work", "sleep", "eat", "coffee", "tired"],
        "travel": ["ticket", "plane", "passport", "hotel", "map", "lost", "visit"],
    }

    GRAMMAR_RULES = {
        "A1": ["Present Simple", "Present Continuous"],
        "A2": ["Past Simple", "Future Simple"],
        "B1": ["Present Perfect", "Past Continuous"]
    }

    def generate_structure(self, request: StoryRequest) -> Dict[str, Any]:
        """
        Создает 'Скелет' истории.
        """
        topic = request.topic.lower()
        level = request.level
        
        # 1. Выбор слов (3-5 штук)
        available_vocab = self.VOCAB_DB.get(topic, ["thing", "good", "day"])
        selected_vocab = random.sample(available_vocab, k=min(4, len(available_vocab)))

        # 2. Выбор грамматики
        available_grammar = self.GRAMMAR_RULES.get(level, ["Present Simple"])
        grammar_focus = random.choice(available_grammar)

        # 3. Инструкции для LLM (System Prompt constraints)
        constraints = {
            "topic": topic,
            "vocab": selected_vocab,
            "grammar": grammar_focus,
            "length": 100 if level == "A1" else 150,
            "cefr_level": level
        }

        return constraints
