# AI Filesystem Agent

This is my project for the AI Systems course. It's an intelligent agent that can perform file operations securely. I built it using Google ADK, Python, and Docker.

## What it does

The agent acts like a sysadmin assistant. You can ask it to:
- List files in directories
- Search for specific files
- Read file contents
- Verify flags (without seeing the content)

It uses a local **Ollama** instance (running Qwen2.5:14b) for reasoning and a custom **MCP Server** for file operations.

## Architecture

- **adk-web**: The brain (Google ADK agent).
- **mcp-server**: The hands (FastMCP server doing the actual file work).
- **ollama**: The LLM engine.

## Setup

You need Docker installed.

1. Clone the repo.
2. Run:
   ```bash
   docker-compose up --build
   ```

*Note: First run takes time because it downloads the 8GB LLM model.*

## Usage

Everything runs on `http://localhost:8080`.

Try asking:
> "Find requirements.txt and tell me what's inside."
> "Is the flag in flag.txt 'SECRET_KEY'?"

## Security

I implemented a few guardrails:
- **Read-only**: The agent can't modify files.
- **Sandboxed**: It can't access files outside the project folder.
- **Protected Files**: `flag.txt` helps test that the agent respects privacy rules.

## Tech Stack

- Python 3.11
- Google ADK
- Model Context Protocol (FastMCP)
- Docker

