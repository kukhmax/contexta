import os
import redis.asyncio as redis
import json
from typing import Optional
import hashlib

class CacheService:
    def __init__(self):
        self.redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
        try:
            self.redis = redis.from_url(self.redis_url, decode_responses=True)
        except Exception as e:
            print(f"Redis init warning: {e}")
            self.redis = None

    async def get_story(self, topic: str, level: str, language: str) -> Optional[dict]:
        """
        Пытается найти историю в кэше.
        Ключ: story:{lang}:{level}:{topic__hash}
        """
        if not self.redis:
            return None
            
        key = self._generate_key(topic, level, language)
        try:
            data = await self.redis.get(key)
            if data:
                return json.loads(data)
        except Exception as e:
            print(f"Redis get error: {e}")
        return None

    async def save_story(self, topic: str, level: str, language: str, story_data: dict, expire_seconds=86400 * 7):
        """
        Сохраняет историю в кэш на 7 дней.
        """
        if not self.redis:
            return
            
        key = self._generate_key(topic, level, language)
        try:
            await self.redis.set(key, json.dumps(story_data), ex=expire_seconds)
        except Exception as e:
            print(f"Redis save error: {e}")

    def _generate_key(self, topic: str, level: str, language: str) -> str:
        # Нормализуем топик (lower case, strip)
        topic_norm = topic.strip().lower()
        # Хеш для безопасности ключа
        topic_hash = hashlib.md5(topic_norm.encode()).hexdigest()
        return f"story:{language}:{level}:{topic_hash}"
