FROM ollama/ollama:latest

# Set host to allow external access
ENV OLLAMA_HOST=0.0.0.0:11434

EXPOSE 11434

# Model will be downloaded on first use or manually after startup
CMD ["serve"]

