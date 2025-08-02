"""
Sentiment Analyzer MCP Server

This MCP server exposes a sentiment analysis API as tools that can be used by LLMs.
The server connects to a sentiment analysis API that classifies text as positive or negative.

Usage:
    python sentiment_mcp_server.py

Or install in Claude Desktop:
    uv run mcp install sentiment_mcp_server.py --name "Sentiment Analyzer" -v API_BASE_URL=http://localhost:8000
"""

import asyncio
import os
from typing import Dict, Any
import aiohttp
from pydantic import BaseModel, Field

from mcp.server.fastmcp import FastMCP

# Configuration
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")

# Create the MCP server
mcp = FastMCP(
    name="Sentiment Analyzer"
)


class SentimentResult(BaseModel):
    """Structured result for sentiment analysis."""
    
    text: str = Field(description="The input text that was analyzed")
    sentiment: str = Field(description="The predicted sentiment (positive/negative)")
    confidence: float | None = Field(default=None, description="Confidence score if available")
    api_response: Dict[str, Any] = Field(description="Full API response for debugging")


@mcp.tool()
async def analyze_sentiment(text: str) -> SentimentResult:
    """
    Analyze the sentiment of input text using a pretrained deep learning model.
    
    This tool sends text to a sentiment analysis API and returns whether the sentiment
    is positive or negative. Useful for understanding the emotional tone of text,
    customer feedback, social media posts, reviews, etc.
    
    Args:
        text: The text to analyze for sentiment
        
    Returns:
        SentimentResult with the predicted sentiment and additional metadata
    """
    if not text.strip():
        raise ValueError("Text cannot be empty")
    
    # Prepare the request payload matching the API schema
    payload = {"text": text}
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{API_BASE_URL}/predict",
                json=payload,
                headers={"Content-Type": "application/json"}
            ) as response:
                
                if response.status == 422:
                    error_data = await response.json()
                    raise ValueError(f"Validation error: {error_data}")
                elif response.status != 200:
                    raise RuntimeError(f"API request failed with status {response.status}: {await response.text()}")
                
                result = await response.json()
                
                return SentimentResult(
                    text=text,
                    sentiment=result["sentiment"],
                    api_response=result
                )
                
    except aiohttp.ClientError as e:
        raise RuntimeError(f"Failed to connect to sentiment analysis API at {API_BASE_URL}: {str(e)}")
    except Exception as e:
        raise RuntimeError(f"Unexpected error during sentiment analysis: {str(e)}")


@mcp.tool()
async def batch_analyze_sentiment(texts: list[str]) -> list[SentimentResult]:
    """
    Analyze sentiment for multiple texts in parallel.
    
    This tool takes a list of texts and analyzes the sentiment of each one,
    processing them concurrently for better performance.
    
    Args:
        texts: List of texts to analyze for sentiment
        
    Returns:
        List of SentimentResult objects, one for each input text
    """
    if not texts:
        raise ValueError("Text list cannot be empty")
    
    if len(texts) > 50:  # Reasonable limit to prevent abuse
        raise ValueError("Maximum 50 texts allowed per batch")
    
    # Process all texts concurrently
    tasks = [analyze_sentiment(text) for text in texts]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    # Handle any exceptions that occurred
    final_results = []
    for i, result in enumerate(results):
        if isinstance(result, Exception):
            # Create error result for failed analysis
            final_results.append(SentimentResult(
                text=texts[i],
                sentiment="error",
                api_response={"error": str(result)}
            ))
        else:
            final_results.append(result)
    
    return final_results


@mcp.tool()
async def check_api_health() -> dict[str, Any]:
    """
    Check if the sentiment analysis API is available and responding.
    
    This tool performs a health check on the sentiment analysis API to verify
    it's accessible and working properly.
    
    Returns:
        Dictionary with health status information
    """
    try:
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=10)) as session:
            # Try a simple prediction to verify the API is working
            test_payload = {"text": "This is a test"}
            
            async with session.post(
                f"{API_BASE_URL}/predict",
                json=test_payload,
                headers={"Content-Type": "application/json"}
            ) as response:
                
                if response.status == 200:
                    result = await response.json()
                    return {
                        "status": "healthy",
                        "api_url": API_BASE_URL,
                        "response_time_ms": response.headers.get("X-Response-Time"),
                        "test_result": result
                    }
                else:
                    return {
                        "status": "unhealthy",
                        "api_url": API_BASE_URL,
                        "error": f"HTTP {response.status}: {await response.text()}"
                    }
                    
    except asyncio.TimeoutError:
        return {
            "status": "timeout",
            "api_url": API_BASE_URL,
            "error": "API request timed out after 10 seconds"
        }
    except aiohttp.ClientError as e:
        return {
            "status": "connection_error",
            "api_url": API_BASE_URL,
            "error": f"Failed to connect: {str(e)}"
        }
    except Exception as e:
        return {
            "status": "error",
            "api_url": API_BASE_URL,
            "error": f"Unexpected error: {str(e)}"
        }


# Add a resource that provides information about the API
@mcp.resource("sentiment://api/info")
def get_api_info() -> str:
    """Get information about the sentiment analysis API."""
    return f"""# Sentiment Analysis API Information

**Base URL**: {API_BASE_URL}
**API Version**: 1.0.0

## Available Endpoints

### POST /predict
Predicts the sentiment (positive/negative) of provided text using a pretrained deep learning model.

**Request Body**:
```json
{{
  "text": "Your text to analyze"
}}
```

**Response**:
```json
{{
  "sentiment": "positive" | "negative"
}}
```

## Usage Notes
- The API uses a pretrained deep learning model for sentiment classification
- Supports text in various formats and lengths
- Returns binary classification: positive or negative
- Response time typically under 1 second for standard text lengths

## Error Handling
- 422: Validation Error (invalid request format)
- 500: Internal Server Error (model processing failed)
"""


@mcp.resource("sentiment://examples")
def get_examples() -> str:
    """Get example usage scenarios for sentiment analysis."""
    return """# Sentiment Analysis Examples

## Positive Examples
- "I love this product! It works perfectly and exceeded my expectations."
- "What a beautiful day! The weather is amazing."
- "Thank you so much for your help. You're the best!"
- "This movie was absolutely fantastic. Highly recommend!"

## Negative Examples  
- "This is the worst service I've ever experienced."
- "I'm really disappointed with this purchase. It broke immediately."
- "The weather is terrible today. Rain and cold."
- "This software is buggy and unreliable."

## Neutral/Mixed Examples (may vary in classification)
- "The product is okay, nothing special."
- "It works as expected, no complaints."
- "Standard quality for the price."
- "The meeting was informative but long."

## Use Cases
- **Customer Feedback**: Analyze reviews and support tickets
- **Social Media Monitoring**: Track brand sentiment on platforms
- **Content Moderation**: Identify potentially negative content
- **Market Research**: Understand public opinion about products/services
- **Email Analysis**: Classify customer emails by sentiment
"""


def main():
    """Entry point for the sentiment analyzer MCP server."""
    print(f"Starting Sentiment Analyzer MCP Server...")
    print(f"API Base URL: {API_BASE_URL}")
    print("Use 'uv run mcp dev sentiment_mcp_server.py' to test with MCP Inspector")
    print("Or install with: uv run mcp install sentiment_mcp_server.py --name 'Sentiment Analyzer'")
    
    mcp.run()


if __name__ == "__main__":
    main()