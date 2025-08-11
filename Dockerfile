FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y netcat-openbsd curl && \
    rm -rf /var/lib/apt/lists/*

# Install uv using standalone installer
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

# Add uv to PATH
ENV PATH="/root/.local/bin:$PATH"

# Copy dependency files first for better Docker cache usage
COPY pyproject.toml uv.lock /app/

# Install Python dependencies using uv
RUN uv sync --frozen

# Copy application code
COPY . /app

# No need to chmod or run wait-for-mongo.sh

CMD ["uv", "run", "python", "-m", "uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]
