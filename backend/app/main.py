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

from app.services.cache import CacheService

# ... (Previous imports)

app = FastAPI(
    title="Make Story AI API",
    version="0.1.0",
    description="API for Android Language Learning App"
)

# ... (Mount static & CORS)

rule_generator = RuleBasedGenerator()
llm_service = LLMService()
nlp_service = NLPService()
tts_service = TTSService()
cache_service = CacheService()

@app.post("/api/v1/generate", response_model=GeneratedStory)
async def generate_story(request: StoryRequest):
    """
    Полный цикл генерации истории.
    1. Проверка КЭША (Redis).
    2. Если нет -> Генерация (Rules -> LLM -> NLP -> TTS).
    3. Сохранение в КЭШ.
    """
    # 1. Проверяем кэш
    cached_story = await cache_service.get_story(request.topic, request.level, request.language)
    if cached_story:
        print("⚡ Cache Hit!")
        return GeneratedStory(**cached_story)

    print("🐢 Cache Miss. Generating...")

    # 2. Структура (Rules)
    constraints = rule_generator.generate_structure(request)
    
    # 3. Текст (LLM)
    raw_text = await llm_service.generate_story_text(constraints)
    
    # 4. Обработка (NLP)
    processed_html, forms = nlp_service.process_story(raw_text, constraints)
    
    # 5. Аудио (TTS)
    audio_path = await tts_service.generate_audio(raw_text, request.language)
    
    # Собираем ответ
    story_response = GeneratedStory(
        title=f"{constraints['topic'].title()} Story",
        story_html=f"<p>{processed_html}</p>",
        forms=forms,
        audio_url=audio_path
    )
    
    # 6. Сохраняем в кэш (преобразуем модель в dict)
    await cache_service.save_story(
        request.topic, 
        request.level, 
        request.language, 
        story_response.model_dump()
    )
    
    return story_response

@app.get("/")
async def root():
    return {"message": "Make Story AI Backend is Running 🚀"}

@app.get("/health")
async def health():
    return {"status": "ok"}
