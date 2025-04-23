"""
Tool for running Aider AI coding tasks.
"""

import os
from typing import List, Optional, Dict
from aider.models import Model
from aider.io import InputOutput
from aider.coders import Coder
from dotenv import load_dotenv

from aider_mcp_server.capabilities.data_types import AICodeParams


def add_thinking_budget_to_params(params: Dict, budget_tokens: int) -> Dict:
    """
    Add thinking budget configuration to model parameters.
    
    Args:
        params: Existing parameters dictionary
        budget_tokens: Number of tokens for thinking budget
        
    Returns:
        Updated parameters dictionary
    """
    updated_params = params.copy()
    updated_params["thinking"] = {"budget": budget_tokens}
    return updated_params


def build_ai_coding_assistant(params: AICodeParams) -> Coder:
    """
    Create and configure a Coder instance based on provided parameters.
    
    Args:
        params: Parameters for configuring the AI coding assistant
        
    Returns:
        Configured Coder instance
    """
    settings = params.settings or {}
    auto_commits = settings.get("auto_commits", False)
    suggest_shell_commands = settings.get("suggest_shell_commands", False)
    detect_urls = settings.get("detect_urls", False)

    # Extract budget_tokens setting once for both models
    budget_tokens = settings.get("budget_tokens")

    if params.architect and params.editor_model:
        model = Model(model=params.model, editor_model=params.editor_model)
        extra_params = {}

        # Add reasoning_effort if available
        if settings.get("reasoning_effort"):
            extra_params["reasoning_effort"] = settings["reasoning_effort"]

        # Add thinking budget if specified
        if budget_tokens is not None:
            extra_params = add_thinking_budget_to_params(extra_params, budget_tokens)

        model.extra_params = extra_params
        return Coder.create(
            main_model=model,
            edit_format="architect",
            io=InputOutput(yes=True),
            fnames=params.editable_context,
            read_only_fnames=params.readonly_context,
            auto_commits=auto_commits,
            suggest_shell_commands=suggest_shell_commands,
            detect_urls=detect_urls,
            use_git=params.use_git,
        )
    else:
        model = Model(params.model)
        extra_params = {}

        # Add reasoning_effort if available
        if settings.get("reasoning_effort"):
            extra_params["reasoning_effort"] = settings["reasoning_effort"]

        # Add thinking budget if specified
        if budget_tokens is not None:
            extra_params = add_thinking_budget_to_params(extra_params, budget_tokens)

        model.extra_params = extra_params
        return Coder.create(
            main_model=model,
            io=InputOutput(yes=True),
            fnames=params.editable_context,
            read_only_fnames=params.readonly_context,
            auto_commits=auto_commits,
            suggest_shell_commands=suggest_shell_commands,
            detect_urls=detect_urls,
            use_git=params.use_git,
        )


def ai_code(coder: Coder, params: AICodeParams) -> None:
    """
    Execute AI coding using provided coder instance and parameters.
    
    Args:
        coder: Configured Coder instance
        params: Parameters for the AI coding task
    """
    # Execute the AI coding with the provided prompt
    coder.run(params.prompt)


def code_with_aider(
    ai_coding_prompt: str, 
    relative_editable_files: List[str], 
    relative_readonly_files: List[str] = None,
    settings: Optional[Dict] = None,
    editor_model: str = None,
    architect_model: Optional[str] = None,
    current_working_dir: str = "."
) -> str:
    """
    Run one-shot Aider based AI coding task.
    
    Args:
        ai_coding_prompt: The prompt for the AI coding task
        relative_editable_files: List of files that can be edited
        relative_readonly_files: List of files that should be read-only
        settings: Optional settings for the Aider session
        editor_model: Model to use for editing
        architect_model: Model to use for architecture (optional)
        current_working_dir: Current working directory
        
    Returns:
        A string indicating success or failure
    """
    # Load environment variables
    load_dotenv()
    
    # Make paths absolute based on current_working_dir
    editable_files = [os.path.join(current_working_dir, file) for file in relative_editable_files]
    readonly_files = []
    if relative_readonly_files:
        readonly_files = [os.path.join(current_working_dir, file) for file in relative_readonly_files]
    
    # Configure whether to use architect mode
    use_architect = architect_model is not None
    
    # Default model if none provided
    default_model = "gpt-4"
    model_to_use = architect_model if use_architect else editor_model
    if model_to_use is None:
        model_to_use = default_model
    
    # Prepare params
    params = AICodeParams(
        architect=use_architect,
        prompt=ai_coding_prompt,
        model=model_to_use,
        editor_model=editor_model if use_architect else None,
        editable_context=editable_files,
        readonly_context=readonly_files,
        settings=settings,
        use_git=settings.get("use_git", False) if settings else False
    )
    
    try:
        # Create coder instance
        coder = build_ai_coding_assistant(params)
        
        # Run AI coding
        ai_code(coder, params)
        
        return "success"
    except Exception as e:
        print(f"Error in code_with_aider: {str(e)}")
        return "failure"