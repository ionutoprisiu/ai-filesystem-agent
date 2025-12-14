FROM python:3.11-slim

WORKDIR /app

# Install curl for health checks
RUN apt-get update && apt-get install -y --fix-missing curl && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy server file
COPY server.py .

EXPOSE 8000

# Environment variable for access key (can be overridden in docker-compose)
ENV MCP_ACCESS_KEY=your-secret-key-here

CMD ["python", "server.py"]

