from fastapi import APIRouter, HTTPException
from .schemas import SentimentRequest, SentimentResponse
from .utils import parse_sentiment_output
from .model_loader import SentimentPipelineLoader

router = APIRouter()
sentiment_pipeline_loader = SentimentPipelineLoader()  # Singleton loader

@router.post("/analyze_sentiment", response_model=SentimentResponse)
def analyze_sentiment(request: SentimentRequest):
    try:
        sentiment_pipeline = sentiment_pipeline_loader.get()
        prediction = sentiment_pipeline(request.text)[0]
        sentiment, confidence = parse_sentiment_output(prediction)
        return SentimentResponse(sentiment=sentiment, confidence=confidence)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Sentiment analysis failed: {str(e)}")
