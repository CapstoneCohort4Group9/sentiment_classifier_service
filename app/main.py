import logging
import time
from contextlib import asynccontextmanager
from fastapi import FastAPI
from .routes import router, sentiment_pipeline_loader

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global variable to track model loading status
model_loaded = False
model_load_error = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    global model_loaded, model_load_error
    logger.info("🚀 Starting model preloading...")
    start_time = time.time()
    
    try:
        # Force eager load at startup
        sentiment_pipeline_loader.load()
        
        # Test the model with a simple prediction
        pipeline = sentiment_pipeline_loader.get()
        test_result = pipeline("test")
        
        load_time = time.time() - start_time
        model_loaded = True
        logger.info(f"✅ Model loaded successfully in {load_time:.2f} seconds")
        logger.info(f"📊 Test prediction: {test_result}")
        
    except Exception as e:
        model_load_error = str(e)
        logger.error(f"❌ Failed to load model: {e}")
        # Don't raise the exception - let the app start but mark as failed
    
    # Yield control to FastAPI
    yield
    
    # Shutdown (cleanup if needed)
    logger.info("🛑 Shutting down...")
    # Add any cleanup code here if needed

app = FastAPI(
    title="Sentiment Analysis API",
    version="1.0",
    description="API to analyze sentiment using RoBERTa-based HuggingFace model",
    lifespan=lifespan
)

@app.get("/model-status")
async def model_status():
    """Check if the model is loaded and ready"""
    return {
        "model_loaded": model_loaded,
        "error": model_load_error,
        "status": "ready" if model_loaded else "loading" if model_load_error is None else "error"
    }

# Register router
app.include_router(router)