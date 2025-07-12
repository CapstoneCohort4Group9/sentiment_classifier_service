import logging
import time
from contextlib import asynccontextmanager
from fastapi import FastAPI
from .routes import sentiment_pipeline_loader

# Configure logging
logger = logging.getLogger(__name__)

# Global variable to track model loading status
model_loaded = False
model_load_error = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for FastAPI application.
    Handles startup and shutdown events.
    """
    # Startup
    global model_loaded, model_load_error
    logger.info("🚀 Starting application lifespan - model preloading...")
    startup_start = time.time()
    
    try:
        # Force eager load at startup
        logger.info("📥 Loading sentiment analysis model...")
        sentiment_pipeline_loader.load()
        
        # Test the model with a simple prediction
        logger.info("🧪 Testing model with sample prediction...")
        pipeline = sentiment_pipeline_loader.get()
        test_result = pipeline("test")
        
        startup_time = time.time() - startup_start
        model_loaded = True
        logger.info(f"✅ Model loaded successfully in {startup_time:.2f} seconds")
        logger.info(f"📊 Test prediction result: {test_result}")
        logger.info("🎯 Application ready to serve requests!")
        
    except Exception as e:
        model_load_error = str(e)
        logger.error(f"❌ Failed to load model during startup: {e}")
        logger.warning("⚠️ Application will start but sentiment analysis will be unavailable")
        # Don't raise the exception - let the app start but mark as failed
    
    # Yield control to FastAPI - application runs here
    yield
    
    # Shutdown
    logger.info("🛑 Starting application shutdown...")
    try:
        # Add any cleanup code here if needed
        # For example: closing database connections, saving state, etc.
        logger.info("🧹 Performing cleanup...")
        
        # Reset global state
        global model_loaded, model_load_error
        model_loaded = False
        model_load_error = None
        
        logger.info("✅ Shutdown completed successfully")
    except Exception as e:
        logger.error(f"❌ Error during shutdown: {e}")

def get_model_status():
    """Get current model loading status"""
    return {
        "model_loaded": model_loaded,
        "error": model_load_error,
        "status": "ready" if model_loaded else "loading" if model_load_error is None else "error"
    }