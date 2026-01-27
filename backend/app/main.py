from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.models.schemas import StoryRequest, GeneratedStory, WordForm

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

@app.post("/api/v1/generate", response_model=GeneratedStory)
async def generate_story(request: StoryRequest):
    """
    Эндпоинт для генерации истории.
    Пока возвращает Mock-данные для разработки Android клиента.
    """
    return GeneratedStory(
        title=f"Mock Story about {request.topic}",
        story_html=f"<p>This is a <b>{request.level}</b> story about {request.topic}. He <mark>went</mark> to the shop.</p>",
        forms=[
            WordForm(form="went", base="go", tense="past simple", translation="ходил")
        ],
        audio_url="https://www2.cs.uic.edu/~i101/SoundFiles/BabyElephantWalk60.wav" # Mock audio
    )

@app.get("/")
async def root():
    return {"message": "Make Story AI Backend is Running 🚀"}

@app.get("/health")
async def health():
    return {"status": "ok"}
