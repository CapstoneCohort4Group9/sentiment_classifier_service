LABEL_MAP = {
    "LABEL_0": "Negative",
    "LABEL_1": "Neutral",
    "LABEL_2": "Positive"
}

def parse_sentiment_output(prediction):
    label = LABEL_MAP.get(prediction["label"], prediction["label"])
    score = prediction["score"]
    return label, score
