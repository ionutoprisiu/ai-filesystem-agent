FROM python:3.11-slim

WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy agent files (using direct HTTP, no bridge)
COPY agents/ ./agents/

EXPOSE 8080

# Environment variables
ENV OLLAMA_URL=http://ollama:11434/v1
ENV MCP_SERVER_URL=http://mcp-server:8000
ENV MCP_ACCESS_KEY=your-secret-key-here

CMD ["adk", "web", "--host", "0.0.0.0", "--port", "8080"]

