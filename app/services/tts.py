import edge_tts
import uuid
import os

class TTSService:
    def __init__(self):
        self.output_dir = "static/audio"
        os.makedirs(self.output_dir, exist_ok=True)
        # Voice mapping: EN, ES, DE, FR patterns
        self.voice_map = {
            "en": "en-US-ChristopherNeural", # Good male voice
            "es": "es-ES-AlvaroNeural",
            "de": "de-DE-ConradNeural",
            "fr": "fr-FR-HenriNeural"
        }

    async def generate_audio(self, text: str, language: str = "en") -> str:
        """
        Generates audio file and returns the relative URL.
        """
        voice = self.voice_map.get(language, "en-US-ChristopherNeural")
        filename = f"{uuid.uuid4()}.mp3"
        filepath = os.path.join(self.output_dir, filename)
        
        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(filepath)
        
        return f"/static/audio/{filename}"
