from fastapi import FastAPI
from .routes import router, sentiment_pipeline_loader

app = FastAPI(
    title="Sentiment Analysis API",
    version="1.0",
    description="API to analyze sentiment using RoBERTa-based HuggingFace model"
)

# Register router
app.include_router(router)

@app.on_event("startup")
async def preload_model():
    sentiment_pipeline_loader.load()  # Force eager load at startup
