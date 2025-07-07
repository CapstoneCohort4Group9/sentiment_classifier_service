from transformers import pipeline

class SentimentPipelineLoader:
    def __init__(self):
        self._pipeline = None

    def load(self):
        if self._pipeline is None:
            self._pipeline = pipeline(
                "sentiment-analysis",
                model="cardiffnlp/twitter-roberta-base-sentiment",
                tokenizer="cardiffnlp/twitter-roberta-base-sentiment"
            )

    def get(self):
        if self._pipeline is None:
            self.load()
        return self._pipeline
