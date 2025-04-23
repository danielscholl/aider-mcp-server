# Specification for Aider (MCP)
> We are building a MCP Server tool for an experimental ai coding mcp server using aider.

## Overview

Claude Code is a new, powerful agentic coding tool that is currently in beta. It's great but it's incredibly expensive. We can offload some of the work to a simpler ai coding tool: Aider. The original AI Coding Assistant.

By discretely offloading work to Aider, we can not only reduce costs but use Claude Code (and auxillary LLM calls combined with aider) to better create more, reliable code through multiple - focused - LLM calls.

## Broad Implementation details

- First, READ ai_docs/* to understand a sample mcp server using fastmcp.
- Mirror the work done inside `of ai_docs/mcp-mem0.xml`. Here we have a complete example of how to build a mcp server. We also have a complete codebase structure that we want to replicate. With some slight tweaks - see `Codebase Structure` below.
- Be sure to use load_dotenv() in the tests.
- Be sure to comment every function and class with clear doc strings.
- Don't mock any tests - run real commands and expect them to pass case insensitive.
- Document the usage of the MCP server in the README.md
- Every capability must be tested in a respective tests directory structure.
- Every capability/tools/*.py must only have a single responsibility - one method.
- If for whatever reason you need additional python packages use uv add <package_name>.
- Setup directions should be simple
  - git clone
  - uv pip install -e .
  - test uv run pytest
  - run uv run python -m aider_mcp_server

### Specific Implementation Details

- When we run aider run in no commit mode, we should not commit any changes to the codebase.
- If architect_model is not provided, don't use architect mode.
- Every cpability must be tested in a respective tests/*_test.py file.
- every capability/tools/*.py must only have a single responsibility - one method.
- requires-python = ">=3.12"
- dependencies
  - aider-chat>=0.82.2
  - fastmcp>=2.2.1
  - pydantic>=2.11.3

## Codebase Structure

- src/
  - aider_mcp_server/
    - __init__.py
    - __main__.py
    - server.py
      - serve(editor_model: str = DEFAULT_EDITOR_MODEL, current_working_dir: str = ".", architect_model: str = None) -> None
    - capabilities/
      - __init__.py
      - tools/
        - __init__.py
        - aider_ai_code.py
          - code_with_aider(ai_coding_prompt: str, relative_editable_files: List[str], relative_readonly_files: List[str] = []) -> str
            - runs one shot aider based on ai_docs/programmable-aider-documentation.md
            - outputs 'success' or 'failure'
        - aider_list_models.py
          - list_models(substring: str) -> List[str]
            - calls aider.models.fuzzy_match_models(substr: str) and returns the list of models
      - utils.py
        - DEFAULT_EDITOR_MODEL = "gemini/gemini-2.5-pro-exp-03-25"
        - DEFAULT_ARCHITECT_MODEL = "gemini/gemini-2.5-pro-exp-03-25"
      - data_types.py
    - tests/
      - __init__.py
      - capabilities/
        - __init__.py
        - tools/
          - __init__.py
          - test_aider_ai_code.py
            - here create tests for basic 'math' functionality: 'add, 'subtract', 'multiply', 'divide'. Use temp dirs.
          - test_aider_list_models.py
            - here create a real call to list_models(openai) and assert gpt-4o substr in list.

## MCP Integration Details

- Include a .mcp.json file for quick setup with MCP clients
- Document multiple ways to integrate with common MCP clients including:
  - SSE transport configuration
  - stdio transport configuration
  - Docker container integration
- Note that this is an MCP server without traditional CLI functionality (no --help flag)
- Update the tool schema in .mcp.json to include the settings parameter in the code_with_aider tool:

## Validation (close the loop)

- Use `uv run pytest <path_to_test_file.py>` to run tests. Every atom/ must be tested.
- Don't mock any tests - run real LLM calls. Make sure to test for failure paths.
- At the end run `uv run aider-mcp-server --help` to validate the server is working.