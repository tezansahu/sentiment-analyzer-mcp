# Sentiment Analyzer with MCP Integration

A complete sentiment analysis solution featuring a deep learning model served via FastAPI and integrated with VS Code through a Model Context Protocol (MCP) server.

## Components

- **`app/`** - FastAPI server hosting the sentiment analysis deep learning model
- **`mcp_server/`** - MCP server that exposes sentiment analysis tools to VS Code/GitHub Copilot

## Quick Start

1. **Start the FastAPI server:**
   ```cmd
   cd app
   .\.venv\Scripts\activate
   uvicorn main:app --reload
   ```

2. **Configure and start the MCP server:**
   ```cmd
   cd mcp_server
   pip install -r requirements.txt
   ```
   
   Add to `.vscode/mcp.json`:
   ```json
   {
       "servers": {
           "sentiment-analyzer": {
               "command": "cmd",
               "args": ["/c", ".\\.venv\\Scripts\\activate.bat && uv run mcp run mcp_server.py"]
           }
       }
   }
   ```

3. **Use in VS Code with GitHub Copilot:**
   - Start the MCP server from VS Code Command Palette
   - Ask Copilot: "Analyze the sentiment of this text: 'I love this product!'"

## Features

- Real-time sentiment analysis (positive/negative classification)
- Batch processing for multiple texts
- Natural language interaction through GitHub Copilot
- Health monitoring and error handling
- Deep learning model with pre-trained weights

For detailed setup instructions, see the README files in each component directory.
