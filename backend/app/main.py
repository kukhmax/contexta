from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from app.models.schemas import StoryRequest, GeneratedStory, WordForm
from app.services.generator_rules import RuleBasedGenerator
from app.services.llm import LLMService
from app.services.nlp_processor import NLPService
from app.services.tts import TTSService

app = FastAPI(
    title="Make Story AI API",
    version="0.1.0",
    description="API for Android Language Learning App"
)

# Mount static for audio
app.mount("/static", StaticFiles(directory="backend/static"), name="static")

# CORS (Allow Android emulator/device)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

rule_generator = RuleBasedGenerator()
llm_service = LLMService()
nlp_service = NLPService()
tts_service = TTSService()

@app.post("/api/v1/generate", response_model=GeneratedStory)
async def generate_story(request: StoryRequest):
    """
    Полный цикл генерации истории.
    """
    # 1. Структура (Rules)
    constraints = rule_generator.generate_structure(request)
    
    # 2. Текст (LLM)
    raw_text = await llm_service.generate_story_text(constraints)
    
    # 3. Обработка (NLP)
    processed_html, forms = nlp_service.process_story(raw_text, constraints)
    
    # 4. Аудио (TTS)
    # Важно: для Android эмулятора нужно возвращать полный URL, 
    # но пока вернем относительный, клиент может сам подставить base_url
    audio_path = await tts_service.generate_audio(raw_text, request.language)
    
    # Собираем ответ
    return GeneratedStory(
        title=f"{constraints['topic'].title()} Story",
        story_html=f"<p>{processed_html}</p>",
        forms=forms,
        audio_url=audio_path
    )

@app.get("/")
async def root():
    return {"message": "Make Story AI Backend is Running 🚀"}

@app.get("/health")
async def health():
    return {"status": "ok"}
