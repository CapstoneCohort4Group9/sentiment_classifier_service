import logging
from fastapi import FastAPI
from .routes import router
from .lifespan import lifespan, get_model_status

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Sentiment Analysis API",
    version="1.0",
    description="API to analyze sentiment using RoBERTa-based HuggingFace model",
    lifespan=lifespan
)

@app.get("/model-status")
async def model_status():
    """Check if the model is loaded and ready"""
    return get_model_status()

# Register router
app.include_router(router)