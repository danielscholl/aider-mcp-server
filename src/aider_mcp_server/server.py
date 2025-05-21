"""
Main server module for the Aider MCP server.
"""

import os
import sys
import asyncio
from typing import Optional, List, Dict, Any
from fastmcp import FastMCP, Context
from contextlib import asynccontextmanager
from collections.abc import AsyncIterator
from dataclasses import dataclass
from dotenv import load_dotenv

from aider_mcp_server.capabilities.utils import DEFAULT_EDITOR_MODEL

# Import tools
from aider_mcp_server.capabilities.tools.aider_ai_code import code_with_aider
from aider_mcp_server.capabilities.tools.aider_list_models import list_models
from aider_mcp_server.capabilities.tools.aider_ask import ask_question as ask_question_sync


@dataclass
class AiderContext:
    """Context for the Aider MCP server."""
    editor_model: str
    architect_model: Optional[str]
    current_working_dir: str


@asynccontextmanager
async def aider_lifespan(server: FastMCP, editor_model: str, architect_model: Optional[str] = None, 
                        current_working_dir: str = ".") -> AsyncIterator[AiderContext]:
    """
    Manages the Aider client lifecycle.
    
    Args:
        server: The FastMCP server instance
        editor_model: The model to use for editing
        architect_model: The model to use for architecture (optional)
        current_working_dir: The current working directory
        
    Yields:
        AiderContext: The context containing the Aider configuration
    """
    try:
        yield AiderContext(
            editor_model=editor_model,
            architect_model=architect_model,
            current_working_dir=current_working_dir
        )
    finally:
        # No explicit cleanup needed
        pass


def serve(editor_model: str = DEFAULT_EDITOR_MODEL, 
          current_working_dir: str = ".", 
          architect_model: Optional[str] = None) -> None:
    """
    Start the Aider MCP server.
    
    Args:
        editor_model: The model to use for editing
        current_working_dir: The current working directory
        architect_model: The model to use for architecture (optional)
    """
    # Load environment variables
    load_dotenv()
    
    # Initialize FastMCP server
    # Handle host and port only when using SSE transport
    host = os.getenv("HOST")
    if not host:
        host = "0.0.0.0"
        
    port = os.getenv("PORT")
    if not port:
        port = 8050
    else:
        port = int(port)
    
    # Create a lifespan function that captures our parameters
    # Need to use partial to bind parameters to the context manager
    from functools import partial
    lifespan_with_params = partial(aider_lifespan, 
                                 editor_model=editor_model, 
                                 architect_model=architect_model, 
                                 current_working_dir=current_working_dir)
    
    mcp = FastMCP(
        "aider-mcp",
        description="MCP server for integrating Aider AI coding tools",
        lifespan=lifespan_with_params,
        host=host,
        port=port
    )
    
    # Register tools
    
    @mcp.tool()
    async def ai_code(
        ctx: Context, 
        ai_coding_prompt: str, 
        relative_editable_files: List[str], 
        relative_readonly_files: Optional[List[str]] = None,
        settings: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Run Aider to perform coding tasks.
        
        Args:
            ctx: The MCP context
            ai_coding_prompt: The prompt for the AI coding task
            relative_editable_files: List of files that can be edited
            relative_readonly_files: List of files that should be read-only
            settings: Optional settings for the Aider session
            
        Returns:
            A string indicating success or failure
        """
        aider_ctx = ctx.request_context.lifespan_context
        result = code_with_aider(
            ai_coding_prompt=ai_coding_prompt,
            relative_editable_files=relative_editable_files,
            relative_readonly_files=relative_readonly_files,
            settings=settings,
            editor_model=aider_ctx.editor_model,
            architect_model=aider_ctx.architect_model,
            current_working_dir=aider_ctx.current_working_dir
        )
        return result
    
    @mcp.tool()
    async def get_models(ctx: Context, substring: str) -> list[str]:
        """
        List available Aider models filtered by substring.
        
        Args:
            ctx: The MCP context
            substring: Substring to filter models by
            
        Returns:
            List of matching model names
        """
        return list_models(substring)

    @mcp.tool()
    async def ask_question(ctx: Context, prompt: str, model: str | None = None) -> str:
        """Ask a question using the specified model and return the response."""

        return ask_question_sync(prompt, model)
    
    # Run the server
    transport = os.getenv("TRANSPORT", "sse")
    
    try:
        print(f"Starting server with transport: {transport}", file=sys.stderr)
        if transport.lower() == 'stdio':
            # For stdio, we need to use the specific stdio async method
            print("Using stdio transport", file=sys.stderr)
            asyncio.run(mcp.run_stdio_async())
        else:
            # For SSE, we'll use the specific SSE async method
            print(f"Using SSE transport on {host}:{port}", file=sys.stderr)
            asyncio.run(mcp.run_sse_async())
    except Exception as e:
        print(f"Server error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()