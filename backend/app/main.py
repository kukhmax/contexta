from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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

@app.get("/")
async def root():
    return {"message": "Make Story AI Backend is Running 🚀"}

@app.get("/health")
async def health():
    return {"status": "ok"}
