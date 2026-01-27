from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.models.schemas import StoryRequest, GeneratedStory, WordForm
from app.services.generator_rules import RuleBasedGenerator
from app.services.llm import LLMService

app = FastAPI(
    title="Make Story AI API",
    version="0.1.0",
    description="API for Android Language Learning App"
)

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

@app.post("/api/v1/generate", response_model=GeneratedStory)
async def generate_story(request: StoryRequest):
    """
    Эндпоинт для генерации истории.
    Использует реальную логику (Шаг 1: Правила + Шаг 2: LLM).
    """
    # 1. Генерируем структуру урока (правила)
    constraints = rule_generator.generate_structure(request)
    
    # 2. Генерируем текст истории (LLM)
    story_text = await llm_service.generate_story_text(constraints)
    
    # 3. (Пока заглушка) NLP + Аудио
    # В будущем здесь будет Spacy и TTS
    
    # Собираем ответ
    return GeneratedStory(
        title=f"{constraints['topic'].title()} Story",
        story_html=f"<p>{story_text}</p>", # Пока просто текст
        forms=[
            WordForm(form="mock", base="mock", tense=constraints['grammar'], translation="заглушка")
        ],
        audio_url=None
    )

@app.get("/")
async def root():
    return {"message": "Make Story AI Backend is Running 🚀"}

@app.get("/health")
async def health():
    return {"status": "ok"}
