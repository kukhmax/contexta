import edge_tts
import uuid
import os

class TTSService:
    def __init__(self):
        # Папка для статики (чтобы отдавать файлы)
        self.static_dir = "backend/static/audio"
        os.makedirs(self.static_dir, exist_ok=True)
        
    async def generate_audio(self, text: str, language: str = "en") -> str:
        """
        Генерирует аудио файл и возвращает путь для API.
        """
        # Убираем HTML теги из текста для озвучки
        clean_text = text.replace("<mark>", "").replace("</mark>", "")
        
        filename = f"{uuid.uuid4()}.mp3"
        filepath = os.path.join(self.static_dir, filename)
        
        # Выбор голоса MVP
        voice = "en-US-ChristopherNeural"
        if language == "es": voice = "es-ES-AlvaroNeural"
        
        try:
            communicate = edge_tts.Communicate(clean_text, voice)
            await communicate.save(filepath)
            
            # В продакшене тут был бы S3 URL. В MVP - локальный файл.
            # Для эмулятора Android (10.0.2.2) путь должен быть относительным API
            return f"/static/audio/{filename}" 
        except Exception as e:
            print(f"TTS Error: {e}")
            return ""
