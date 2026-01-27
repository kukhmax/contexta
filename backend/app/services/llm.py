import os
import json
from openai import AsyncOpenAI
from typing import Dict, Any

class LLMService:
    def __init__(self):
        # Используем Compatible API (DeepSeek, перенаправленный через base_url)
        self.api_key = os.getenv("LLM_API_KEY", "sk-mock-key")
        self.base_url = os.getenv("LLM_BASE_URL", "https://api.deepseek.com/v1")
        self.model = os.getenv("LLM_MODEL", "deepseek-chat")
        
        self.client = AsyncOpenAI(api_key=self.api_key, base_url=self.base_url)

    async def generate_story_text(self, constraints: Dict[str, Any]) -> str:
        """
        Шаг 2: Генерация текста истории с помощью LLM (дешевая модель).
        Возвращает чистый текст истории.
        """
        # Если ключа нет - вернем Mock (экономия)
        if self.api_key == "sk-mock-key":
             return self._mock_generation(constraints)

        system_prompt = f"""You are an A1/A2 language teacher.
Write a very short story ({constraints['length']} words) on topic '{constraints['topic']}'.
Level: {constraints['cefr_level']}.
Target Grammar: {constraints['grammar']}.
Target Vocab: {', '.join(constraints['vocab'])}.
Highlight the target vocab verbs in the text by wrapping them in SQL-like brackets like [run].
Keep sentences simple. Return ONLY the story text."""

        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": "Generate story."}
                ],
                temperature=0.7,
                max_tokens=300
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"LLM Error: {e}")
            return self._mock_generation(constraints) # Failover safe

    def _mock_generation(self, constraints: Dict) -> str:
        """Заглушка для тестов без трат денег"""
        vocab_str = ", ".join(constraints['vocab'])
        return f"""
        [MOCK STORY]
        This is a story about {constraints['topic']}.
        It uses {constraints['grammar']}.
        Key words: {vocab_str}.
        He [walked] to the [station] and [saw] a [bus].
        """
