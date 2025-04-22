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
- every tool .py file musst have a respective test .py file.
- every tool .py must only have a single responsibility - one method.
- if for whatever reason you need additional python packages use uv add <package_name>.

### Specific Implementation Details
- when we run aider run in no commit mode, we should not commit any changes to the codebase.
- if architect_model is not provided, don't use architect mode.


## Codebase Structure

- Follow the codebase Structure provided in the mcp-mem0 sample.

## Core Tool Commands to Implement (MVP)

- def list_models(substring: str) -> List[str]:
- def code_with_aider(...)


## MCP Integration Details

- Include a .mcp.json file for quick setup with MCP clients
- Document multiple ways to integrate with common MCP clients including:
  - SSE transport configuration
  - stdio transport configuration
  - Docker container integration
- Note that this is an MCP server without traditional CLI functionality (no --help flag)

## Validation (close the loop)

- Run `uv run pytest <path_to_test>` to validate the tests are passing - do this iteratively as you build out the tests.
- After code is written, run `uv run pytest` to validate all tests are passing.
- To validate the server, start it with `uv run backlog-manager` and connect with an MCP client
- Success criteria:
  - All tests pass
  - Server starts correctly with both transport options
  - All tools function as expected with valid input
  - Error handling works correctly with invalid input
  - JSON data structure maintains integrity