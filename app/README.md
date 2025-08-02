# Sentiment Analyzer FastAPI Server

This project provides a FastAPI server for sentiment analysis using a small, pretrained deep learning model. The server classifies input text as either positive or negative sentiment.

## Features
- `/predict` endpoint for sentiment classification
- Accepts plain text input
- Returns sentiment label (positive/negative)
- OpenAPI documentation auto-generated

## Setup
1. Install dependencies:
   ```cmd
   pip install -r requirements.txt
   ```
2. Start the server:
   ```cmd
   uvicorn main:app --reload
   ```

## API Endpoints
### POST /predict
- **Request Body:**
  - `text`: string (the text to analyze)
- **Response:**
  - `sentiment`: string ("positive" or "negative")

#### Example Request
```json
{
  "text": "I love this product!"
}
```

#### Example Response
```json
{
  "sentiment": "positive"
}
```

## OpenAPI Spec
Visit `/docs` for interactive API documentation and OpenAPI spec.
