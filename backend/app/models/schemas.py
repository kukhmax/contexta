from pydantic import BaseModel, Field
from typing import List, Optional

class StoryRequest(BaseModel):
    topic: str = Field(..., description="Тема истории", example="travel")
    level: str = Field(..., description="Уровень языка (A1, A2, B1)", example="A1")
    language: str = Field(..., description="Целевой язык (en, es, de, fr)", example="en")

class WordForm(BaseModel):
    form: str = Field(..., description="Слово в тексте", example="ran")
    base: str = Field(..., description="Базовая форма", example="run")
    tense: str = Field(..., description="Грамматическая форма", example="past simple")
    translation: str = Field(..., description="Перевод на родной язык", example="бежал")

class GeneratedStory(BaseModel):
    title: str = Field(..., description="Заголовок истории")
    story_html: str = Field(..., description="HTML контент с разметкой для подсветки")
    forms: List[WordForm] = Field(..., description="Список форм для обучения")
    audio_url: Optional[str] = Field(None, description="Ссылка на аудио файл")
