# Aider MCP Server

> A Machine Cognition Protocol (MCP) server that provides AI coding capabilities using Aider.

<p align="center">
  <img src="https://img.shields.io/badge/Status-Beta-yellow" alt="Status: Beta">
  <img src="https://img.shields.io/badge/Python-3.10%2B-green" alt="Python: 3.10+">
</p>

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Server](#running-the-server)
- [MCP Tools](#mcp-tools)
- [Integration with MCP Clients](#integration-with-mcp-clients)
- [Troubleshooting](#troubleshooting)
- [License](#license)

## Overview

This MCP server leverages Aider, a powerful AI coding assistant, to provide coding capabilities via a standardized API. By discretely offloading work to Aider, we can reduce costs while using model-specific capabilities to create more reliable code through multiple focused LLM calls.

## Features

- **AI Code Generation**: Run one-shot coding tasks with Aider to add, fix, or enhance code
- **Model Selection**: Query available models to choose the most appropriate one for your task
- **Flexible Configuration**: Configure Aider sessions with customizable settings
- **Multi-transport Support**: Run via Server-Sent Events (SSE) or stdio for flexible integration

## Prerequisites

- **Python**: 3.10 or higher
- **Package Manager**: uv (recommended) or pip
- **API Keys**: Depending on the models you want to use, you'll need API keys for:
  - OpenAI (for GPT models)
  - Anthropic (for Claude models)
  - Google (for Gemini models)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/aider-mcp.git
   cd aider-mcp
   ```

2. Install the package:
   ```bash
   uv venv
   uv pip install -e .
   ```

3. Run the tests to ensure everything is working:
   ```bash
   uv run pytest
   ```

## Configuration

Configure the server behavior using environment variables in a `.env` file:

```bash
# Create environment file from example
cp .env.example .env
```

Edit the `.env` file to configure transport, host, port, and API keys.

| Variable            | Description                                | Default      | Required |
| ------------------- | ------------------------------------------ | ------------ | -------- |
| `TRANSPORT`         | Transport protocol (sse or stdio)          | `sse`        | No       |
| `HOST`              | Host to bind to when using SSE transport   | `0.0.0.0`    | No       |
| `PORT`              | Port to listen on when using SSE transport | `8050`       | No       |
| `OPENAI_API_KEY`    | API key for OpenAI models                  |              | *        |
| `ANTHROPIC_API_KEY` | API key for Anthropic models               |              | *        |
| `GEMINI_API_KEY`    | API key for Google Gemini models           |              | *        |

*Required only if using models from that provider

### Command Line Options

- `--editor-model`: Model to use for editing (default: gemini/gemini-2.5-pro-exp-03-25)
- `--architect-model`: Model to use for architecture planning (optional)
- `--cwd`: Current working directory (default: current directory)

## Running the Server

### Start the Server (SSE Mode)

```bash
# Using the module directly
uv run python -m aider_mcp_server
```

Or with custom settings:

```bash
uv run python -m aider_mcp_server --editor-model "gemini/gemini-2.5-pro-exp-03-25" --cwd "/path/to/project"
```

You should see output similar to:

```
Starting server with transport: sse
Using SSE transport on 0.0.0.0:8050
```

### Using stdio Mode

When using stdio mode, you don't need to start the server separately - the MCP client will start it automatically when configured properly (see [Integration with MCP Clients](#integration-with-mcp-clients)).

## MCP Tools

The Aider MCP server exposes the following tools:

### ai_code

Run Aider to perform coding tasks.

Parameters:
- `ai_coding_prompt`: The prompt for the AI coding task
- `relative_editable_files`: List of files that can be edited
- `relative_readonly_files`: (Optional) List of files that should be read-only
- `settings`: (Optional) Settings for the Aider session

Example:
```json
{
  "ai_coding_prompt": "Add a function that calculates the factorial of a number",
  "relative_editable_files": ["math.py"],
  "settings": {
    "auto_commits": false,
    "use_git": false
  }
}
```

### get_models

List available Aider models filtered by substring.

Parameters:
- `substring`: Substring to filter models by

Example:
```json
{
  "substring": "openai"
}
```

## Integration with MCP Clients

Configure your MCP client to connect to the SSE endpoint:

```json
{
  "mcpServers": {
    "aider-mcp-server": {
      "transport": "sse",
      "serverUrl": "http://localhost:8050/sse"
    }
  }
}
```

### Stdio Integration

Configure your MCP client to run the server via stdio:

```json
{
  "mcpServers": {
    "aider-mcp-server": {
      "transport": "stdio",
      "command": "python",
      "args": ["-m", "aider_mcp_server"],
      "env": {
        "TRANSPORT": "stdio"
      }
    }
  }
}
```

### Integration with MCP Clients

#### Using Docker 

```json
{
    "mcpServers": {
      "aider-mcp-server": {
        "command": "docker",
        "args": [ "run", "-i", "--rm",
          "--mount", "type=bind,source=<YOUR_FULL_PATH>",
          "-e", "TRANSPORT=stdio",
          "-e", "EDITOR_MODEL=gemini/gemini-2.5-pro-preview-03-25",
          "-e", "GEMINI_API_KEY=<YOUR_API_KEY>",
          "danielscholl/aider-mcp-server"
        ]
      }
    }
  }
```