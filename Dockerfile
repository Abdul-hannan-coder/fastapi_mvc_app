FROM python:3.12-slim

WORKDIR /app

# Install uv and netcat (for wait script)
RUN apt-get update && apt-get install -y netcat-openbsd && pip install uv

# Copy project files for dependency installation
COPY pyproject.toml uv.lock .

# Install dependencies using uv
RUN uv sync --frozen

# Copy the rest of the application code
COPY . .

# Copy wait script
COPY wait-for-mongo.sh .
RUN chmod +x wait-for-mongo.sh

# Expose the port
EXPOSE 8000

# Command to run the FastAPI app with wait script
CMD ["./wait-for-mongo.sh", "uv", "run", "uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]