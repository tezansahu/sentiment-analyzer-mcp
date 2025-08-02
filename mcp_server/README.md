# Sentiment Analyzer MCP Server

This is a Model Context Protocol (MCP) server that provides sentiment analysis capabilities through a local FastAPI server. The server exposes three main tools for analyzing text sentiment using a deep learning model.

## Overview

The Sentiment Analyzer MCP Server acts as a bridge between MCP-compatible clients (like VS Code with GitHub Copilot) and a local sentiment analysis API. The underlying sentiment analysis model is hosted behind a FastAPI server and can classify text as positive or negative.

### Available Tools

1. **`analyze_sentiment`** - Analyze the sentiment of a single text
2. **`batch_analyze_sentiment`** - Analyze sentiment for multiple texts in parallel
3. **`check_api_health`** - Check if the sentiment analysis API is available and responding

### Available Resources

- **`sentiment://api/info`** - Information about the sentiment analysis API
- **`sentiment://examples`** - Example usage scenarios and text samples

## Prerequisites

- Python 3.8+
- [uv](https://docs.astral.sh/uv/) package manager
- VS Code with GitHub Copilot extension
- The sentiment analysis FastAPI server running locally (from the `app/` folder)

## Setup Instructions

### Step 1: Prepare the Sentiment Analysis API

First, ensure the FastAPI sentiment analysis server is running:

```cmd
cd ..\app
.\.venv\Scripts\activate
uvicorn main:app --reload
```

The API should be accessible at `http://localhost:8000`.

### Step 2: Install MCP Server Dependencies

Navigate to the MCP server directory and install dependencies:

```cmd
cd mcp_server
pip install -r requirements.txt
```

### Step 3: Test the MCP Server

Test the MCP server to ensure it works correctly:

```cmd
uv run mcp run mcp_server.py
```

This will start the MCP server and you should see output confirming the server is running and can connect to the sentiment analysis API.

### Step 4: Configure VS Code Integration

Create or update the `.vscode/mcp.json` file in your workspace root:

```json
{
    "servers": {
        "sentiment-analyzer": {
            "command": "cmd",
            "args": [
                "/c",
                ".\\.venv\\Scripts\\activate.bat && uv run mcp run mcp_server\\mcp_server.py"
            ]
        }
    }
}
```

### Step 5: Start the MCP Server in VS Code

1. Open VS Code in your workspace
2. Open the Command Palette (`Ctrl+Shift+P`)
3. Search for "MCP: Manage Servers"
4. Find "sentiment-analyzer" and click "Start"
5. Wait for confirmation that 3 tools have been identified

## Usage Examples

Once the MCP server is running and integrated with VS Code, you can interact with it through GitHub Copilot:

### Basic Sentiment Analysis

```
You: Analyze the sentiment of this text: 'I love this product!'

Copilot: I'll analyze the sentiment of that text for you.

[Calls analyze_sentiment tool]

The sentiment analysis results show:
- Text: "I love this product!"
- Sentiment: positive
- This indicates a positive emotional tone expressing satisfaction and enthusiasm about the product.
```

### Batch Analysis and Sensitivity Testing

```
You: Can you do a sensitivity analysis of this sentiment classification model by testing variations of the same review?

Copilot: I'll test the sentiment classification model with variations of a review to analyze its sensitivity.

[Calls batch_analyze_sentiment tool with variations]

Here's the sensitivity analysis results:
- "I love this product!" → positive
- "I really love this product!" → positive  
- "I kind of love this product." → positive
- "I don't love this product." → negative
- "I love this product?" → positive

The model shows good sensitivity to negations and maintains consistency with intensity variations.
```

## Development Process

This MCP server was created using the following process:

1. **API Specification Extraction**: Obtained the OpenAPI spec from the running FastAPI server:
   ```cmd
   curl -o openapi.json http://localhost:8000/openapi.json
   ```

2. **Documentation Research**: Downloaded relevant documentation:
   - MCP documentation from the [official docs repository](https://github.com/modelcontextprotocol/docs/tree/main)
   - README from the [MCP Python SDK repository](https://github.com/modelcontextprotocol/python-sdk)

3. **Code Generation**: Used Claude AI to generate the MCP server code based on the API specification and documentation ([conversation link](https://claude.ai/share/effc18f9-eb50-41d4-a3b4-24c720460656))

4. **Implementation**: Implemented the generated code in `mcp_server.py`

5. **Testing**: Thoroughly tested the server using `uv run mcp run mcp_server.py`

6. **Integration**: Configured VS Code integration through `.vscode/mcp.json`
