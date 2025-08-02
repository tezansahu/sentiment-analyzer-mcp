from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import pipeline, AutoModelForSequenceClassification, AutoTokenizer
import torch
import os

MODEL_NAME = "distilbert-base-uncased-finetuned-sst-2-english"
MODEL_PATH = "model"

# Download and save model if not already present
def download_model():
    if not os.path.exists(MODEL_PATH):
        os.makedirs(MODEL_PATH)
    if not os.path.exists(os.path.join(MODEL_PATH, "config.json")):
        model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)
        tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
        model.save_pretrained(MODEL_PATH)
        tokenizer.save_pretrained(MODEL_PATH)

download_model()

# Load model and tokenizer from local path
model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH)
tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
sentiment_pipeline = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)

app = FastAPI(
    title="Sentiment Analyzer API",
    description="API for classifying text sentiment as positive or negative using a pretrained deep learning model.",
    version="1.0.0"
)

class TextRequest(BaseModel):
    text: str

class SentimentResponse(BaseModel):
    sentiment: str

@app.post("/predict", response_model=SentimentResponse, summary="Predict sentiment of input text", tags=["Sentiment"])
def predict_sentiment(request: TextRequest):
    """
    Predict the sentiment (positive/negative) of the provided text.
    """
    if not request.text or not request.text.strip():
        raise HTTPException(status_code=400, detail="Text input is required.")
    result = sentiment_pipeline(request.text)[0]
    label = result["label"].lower()
    sentiment = "positive" if label == "positive" else "negative"
    return SentimentResponse(sentiment=sentiment)
