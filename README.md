# Aider MCP Server

A Machine Cognition Protocol (MCP) server that provides AI coding capabilities using Aider.

## Overview

This MCP server leverages Aider, a powerful AI coding assistant, to provide coding capabilities via a standardized API. By discretely offloading work to Aider, we can reduce costs while using model-specific capabilities to create more reliable code through multiple focused LLM calls.

## Features

- **AI Code Generation**: Run one-shot coding tasks with Aider to add, fix, or enhance code
- **Model Selection**: Query available models to choose the most appropriate one for your task
- **Flexible Configuration**: Configure Aider sessions with customizable settings
- **Multi-transport Support**: Run via Server-Sent Events (SSE) or stdio for flexible integration

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

## Usage

### Starting the Server

Run the MCP server:

```bash
uv run python -m aider_mcp_server
```

Or with custom settings:

```bash
uv run python -m aider_mcp_server --editor-model "gemini/gemini-2.5-pro-exp-03-25" --cwd "/path/to/project"
```

### Environment Variables

Copy the `.env.example` file to `.env` and adjust the settings as needed:

```bash
cp .env.example .env
```

Edit the `.env` file to configure transport, host, port, and API keys.

### Command Line Options

- `--editor-model`: Model to use for editing (default: gemini/gemini-2.5-pro-exp-03-25)
- `--architect-model`: Model to use for architecture planning (optional)
- `--cwd`: Current working directory (default: current directory)

## Integration with MCP Clients

### SSE Transport Configuration

Configure your MCP client to connect to the SSE endpoint:

```json
{
  "url": "http://localhost:8050"
}
```

### Stdio Transport Configuration

Configure your MCP client to run the server via stdio:

```json
{
  "command": ["uv", "run", "python", "-m", "aider_mcp_server"]
}
```

### Docker Container Integration

Build and run the Docker container:

```bash
docker build -t aider-mcp:latest .
docker run -p 8050:8050 aider-mcp:latest
```

## Available Tools

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

## License

MIT