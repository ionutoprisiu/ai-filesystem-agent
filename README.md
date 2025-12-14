# AI Filesystem Agent

This is a project I made for a university assignment. It's basically an AI agent that can interact with the filesystem. I used Google ADK with a local LLM (Ollama running Qwen2.5) and an MCP server that provides filesystem tools.

## What it does

The project has 3 main components:
- **Ollama**: Runs the LLM model locally (Qwen2.5:14b)
- **MCP Server**: Provides tools for filesystem operations
- **ADK Web Agent**: The main agent that connects everything

You can ask the agent to list directories, find files, or read file contents. There's also a protected file (flag.txt) that can't be read directly.

## Requirements

You need:
- Docker and Docker Compose
- At least 8GB RAM (the model is pretty big)
- Around 10GB free space for the model

## How to run

1. Clone the repo:
```bash
git clone <repository-url>
cd ai-filesystem-agent
```

2. (Optional) Set the access key if you want:
```bash
export MCP_ACCESS_KEY=your-secret-key-here
```

3. Start everything:
```bash
docker-compose up --build
```

**Note**: The first time you run this, it will download the Qwen2.5:14b model which is about 8GB, so it might take a while depending on your internet.

## Using it

After everything starts up:

1. Open `http://localhost:8080` in your browser
2. You can ask the agent things like:
   - "List all files in the project directory"
   - "Find the file server.py"
   - "Read the contents of requirements.txt"
   - "What's in flag.txt?" (this will be blocked)
   - "Is the flag SECRETKEY?" (this will check without showing the file)

## Project Structure

```
ai-filesystem-agent/
├── adk-web/              # ADK agent
│   ├── agents/
│   │   └── agent.py
│   ├── Dockerfile
│   └── requirements.txt
├── mcp-server/           # MCP server
│   ├── server.py
│   ├── Dockerfile
│   └── requirements.txt
├── ollama/               # Ollama server
│   └── Dockerfile
├── docker-compose.yml
└── README.md
```

## Available Tools

The MCP server has these tools:
- `list_directory(dir_path)` - Lists directory contents
- `list_directory_recursive(dir_path)` - Lists everything recursively
- `find_file(dir_path, filename)` - Finds a file by name
- `get_file_content(file_path)` - Reads a file
- `get_file_head(file_path, num_lines)` - Reads first N lines
- `verify_flag(proposed_flag)` - Checks if a flag is correct

## Security

I added some basic security:
1. Path traversal protection - can't go outside allowed directories
2. Protected files - flag.txt can't be read directly
3. Read-only filesystem - can only read, not write
4. Flag verification - can check if flag is correct without seeing it

## Configuration

You can set environment variables if needed:
- `MCP_ACCESS_KEY` - access key (default: `your-secret-key-here`)
- `OLLAMA_URL` - where Ollama is running (default: `http://ollama:11434/v1`)
- `MCP_SERVER_URL` - where MCP server is (default: `http://mcp-server:8000`)

## Troubleshooting

**Model not downloading?** Try pulling it manually:
```bash
docker exec -it ollama-llama ollama pull qwen2.5:14b
```

**Something not working?** Check the logs:
```bash
docker-compose logs ollama
docker-compose logs mcp-server
docker-compose logs adk-web
```

**Port already in use?** Change the ports in docker-compose.yml

## Running without Docker

If you want to run it locally (I haven't tested this much):

1. Install dependencies:
```bash
cd mcp-server && pip install -r requirements.txt
cd ../adk-web && pip install -r requirements.txt
```

2. You'll need Ollama running separately

3. Start the MCP server:
```bash
cd mcp-server
python server.py
```

4. Start the ADK agent:
```bash
cd adk-web
adk web --host 0.0.0.0 --port 8080
```

## Tech Stack

- Google ADK - for building the agent
- FastMCP - MCP server framework
- Ollama - local LLM server
- LiteLLM - LLM API interface
- Docker - for containers
- Python 3.11

## Known Issues

- Only read access (filesystem is read-only)
- Large files might be slow
- First run needs to download the model (8GB)
- Model quality depends on the local LLM

## Future Improvements

Things I might add later:
- Write operations
- Better authentication
- More file operations
- Support for different models
- Better error handling

---

Built for a university assignment on AI agent development.
