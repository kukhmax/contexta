from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.models.schemas import StoryRequest, StoryStructure
from app.services.generator_rules import RuleBasedGenerator
from app.services.llm import LLMService
from app.services.tts import TTSService

app = FastAPI(title="Make Story AI", description="Low-cost AI story generator")

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

generator_rules = RuleBasedGenerator()
llm_service = LLMService()
nlp_service = NLPService()
tts_service = TTSService()

@app.post("/test/structure", response_model=StoryStructure)
async def test_structure_generation(request: StoryRequest):
    """Test Step 1: Rule-based structure generation"""
    return generator_rules.generate_structure(request)

@app.post("/test/llm")
async def test_llm_generation(structure: StoryStructure):
    """Test Step 2: LLM generation (connects to Step 1 output)"""
    text = await llm_service.generate_story_text(structure)
    return {"story": text}

@app.post("/test/nlp")
async def test_nlp_processing(structure: StoryStructure):
    """Test Step 3: NLP Post-processing (Highlighter)"""
    # 1. Generate text (Mock or Real)
    text = await llm_service.generate_story_text(structure)
    # 2. Process
    result = nlp_service.process_text(text, structure)
    return result

@app.post("/test/audio")
async def test_audio_generation(text: str, language: str = "en"):
    """Test Step 4: Audio Generation"""
    url = await tts_service.generate_audio(text, language)
    return {"audio_url": url}

@app.get("/")
async def read_root():
    return FileResponse("static/index.html")

@app.get("/health")
async def health_check():
    return {"status": "ok", "message": "Service is running"}
