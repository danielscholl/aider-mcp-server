# Specification for Aider (MCP)
> We are building a MCP Server tool for an experimental ai coding mcp server using aider.

## Overview

Claude Code is a new, powerful agentic coding tool that is currently in beta. It's great but it's incredibly expensive. We can offload some of the work to a simpler ai coding tool: Aider. The original AI Coding Assistant.

By discretely offloading work to Aider, we can not only reduce costs but use Claude Code (and auxillary LLM calls combined with aider) to better create more, reliable code through multiple - focused - LLM calls.

## Broad Implementation details

- First, READ ai_docs/* to understand a sample mcp server.
- Mirror the work done inside `of ai_docs/mcp-mem0.xml`. Here we have a complete example of how to build a mcp server. We also have a complete codebase structure that we want to replicate. With some slight tweaks - see `Codebase Structure` below.
- Be sure to use load_dotenv() in the tests.
- Be sure to comment every function and class with clear doc strings.
- Don't mock any tests - run real commands and expect them to pass case insensitive.
- Document the usage of the MCP server in the README.md
- Every capability must be tested in a respective tests directory structure.
- Every capability/tools/*.py must only have a single responsibility - one method.
- If for whatever reason you need additional python packages use uv add <package_name>.

### Specific Implementation Details
- When we run aider run in no commit mode, we should not commit any changes to the codebase.
- If architect_model is not provided, don't use architect mode.
- Include additional configuration parameters for Aider, following the pattern in programmable-aider.md:
  - support for auto_commits (default: False)
  - support for suggest_shell_commands (default: False)
  - support for detect_urls (default: False)
  - support for reasoning_effort parameter
  - support for budget_tokens parameter

## Codebase Structure

- src/
  - aider_mcp_server/
    - __init__.py
    - __main__.py
      - Main entry point for the application
    - config/
      - __init__.py
      - settings.py
        - Configuration settings, including defaults and environment variable handling
    - core/
      - __init__.py
      - data_types.py
        - AiderToolResponse data class
        - AiderMCPContext data class
        - AICodeParams data class following the programmable-aider.md pattern
      - utils.py
        - DEFAULT_EDITOR_MODEL = "gemini/gemini-2.5-pro-exp-03-25"
        - DEFAULT_ARCHITECT_MODEL = "gemini/gemini-2.5-pro-exp-03-25"
        - add_thinking_budget_to_params(params: dict, budget_tokens: int) -> dict
          - Helper function to add thinking budget to the parameters
    - capabilities/
      - __init__.py
      - tools/
        - __init__.py
        - aider_ai_code.py
          - code_with_aider(ai_coding_prompt: str, relative_editable_files: List[str], relative_readonly_files: List[str] = [], editor_model: str = DEFAULT_EDITOR_MODEL, architect_model: str = None, working_dir: str = ".", settings: dict = None) -> str
            - runs one shot aider based on ai_docs/programmable-aider.md
            - outputs 'success' or 'failure'
            - handles all the settings parameters (auto_commits, suggest_shell_commands, detect_urls, reasoning_effort, budget_tokens)
        - aider_list_models.py
          - list_models(substring: str) -> List[str]
            - calls aider.models.fuzzy_match_models(substr: str) and returns the list of models
      - resources/
        - __init__.py
        - aider_resources.py
          - Contains resource helpers for Aider interactions
      - prompts/
        - __init__.py
        - aider_prompts.py
          - Contains any prompts or templates needed for Aider interactions
    - server/
      - __init__.py
      - server.py
        - serve(editor_model: str = DEFAULT_EDITOR_MODEL, current_working_dir: str = ".", architect_model: str = None) -> None
          - MCP server implementation
    - tests/
      - __init__.py
      - core/
        - __init__.py
        - test_utils.py
          - Tests for utility functions
      - capabilities/
        - __init__.py
        - tools/
          - __init__.py
          - test_aider_ai_code.py
            - Create tests for basic 'math' functionality: 'add, 'subtract', 'multiply', 'divide'. Use temp dirs.
            - Test with different settings configurations
          - test_aider_list_models.py
            - Create a real call to list_models(openai) and assert gpt-4o substr in list
        - resources/
          - __init__.py
          - test_aider_resources.py
            - Test resource helper functions
        - prompts/
          - __init__.py
          - test_aider_prompts.py
            - Test template rendering and prompt generation

## Core Tool Commands to Implement (MVP)

- def list_models(substring: str) -> List[str]:
  - Lists models matching the given substring
  - Returns a list of model identifiers
  
- def code_with_aider(ai_coding_prompt: str, relative_editable_files: List[str], relative_readonly_files: List[str] = [], editor_model: str = DEFAULT_EDITOR_MODEL, architect_model: str = None, working_dir: str = ".", settings: dict = None) -> str:
  - Processes the AI coding prompt using Aider
  - Handles file context (editable and read-only)
  - Configures Aider using the settings parameter
  - Returns success/failure status

## MCP Integration Details

- Include a .mcp.json file for quick setup with MCP clients
- Document multiple ways to integrate with common MCP clients including:
  - SSE transport configuration
  - stdio transport configuration
  - Docker container integration
- Note that this is an MCP server without traditional CLI functionality (no --help flag)
- Update the tool schema in .mcp.json to include the settings parameter in the code_with_aider tool:

## Validation (close the loop)

- Run `uv run pytest <path_to_test>` to validate the tests are passing - do this iteratively as you build out the tests.
- After code is written, run `uv run pytest` to validate all tests are passing.
- To validate the server, start it with `python -m aider_mcp_server` and connect with an MCP client
- Success criteria:
  - All tests pass
  - Server starts correctly with both transport options
  - All tools function as expected with valid input
  - Error handling works correctly with invalid input
  - JSON data structure maintains integrity