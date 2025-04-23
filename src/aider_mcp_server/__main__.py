"""
Entry point for the Aider MCP server.
"""

import argparse
import sys
from aider_mcp_server.server import serve
from aider_mcp_server.capabilities.utils import DEFAULT_EDITOR_MODEL


def main():
    """
    Parse command line arguments and start the server.
    """
    parser = argparse.ArgumentParser(description="Aider MCP Server")
    parser.add_argument(
        "--editor-model", 
        type=str, 
        default=DEFAULT_EDITOR_MODEL,
        help=f"Model to use for editing (default: {DEFAULT_EDITOR_MODEL})"
    )
    parser.add_argument(
        "--architect-model", 
        type=str, 
        help="Model to use for architecture planning (optional)"
    )
    parser.add_argument(
        "--cwd", 
        type=str, 
        default=".",
        help="Current working directory (default: current directory)"
    )
    
    # Parse arguments
    args = parser.parse_args()
    
    try:
        # Start the server
        serve(
            editor_model=args.editor_model,
            current_working_dir=args.cwd,
            architect_model=args.architect_model
        )
    except KeyboardInterrupt:
        print("Server stopped by user", file=sys.stderr)
        return 0
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())