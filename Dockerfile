FROM python:3.12-slim

ARG PORT=8050
ENV EDITOR_MODEL="gemini/gemini-2.5-pro-preview-03-25"

# Install uv as root
RUN pip install uv

# Copy the MCP server files
COPY . /app/

# Install packages as root
RUN cd /app && uv pip install --system -e .

# Create a non-root user
RUN useradd -m -s /bin/bash aider
USER aider

# Set the working directory to the mounted workspace
WORKDIR /workspace

EXPOSE ${PORT}

# Command to run the MCP server with the workspace as working directory
CMD ["sh", "-c", "uv run python -m aider_mcp_server --cwd /workspace --editor-model \"$EDITOR_MODEL\""]