FROM python:3.10-slim

# Set working directory
WORKDIR /app

RUN apt-get update && apt-get install -y tzdata && \
    ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    gcc \
    libpq-dev \
    python3-venv \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
ENV POETRY_VERSION=1.8.2
RUN curl -sSL https://install.python-poetry.org | python3 - && \
    ln -s /root/.local/bin/poetry /usr/local/bin/poetry

# Disable Poetry virtualenvs
RUN poetry config virtualenvs.create false

# Copy dependency files first for caching
COPY ./app/pyproject.toml ./app/poetry.lock* /app/

# Install dependencies
RUN poetry install --no-interaction --no-root

# Copy the rest of the code
COPY ./app /app
COPY ./start-server.sh /start-server.sh
COPY ./gunicorn_conf.py /gunicorn_conf.py

# Set permissions
RUN chmod +x /start-server.sh

# Expose port
EXPOSE 8000

# Run the server
CMD ["/bin/bash", "/start-server.sh"]
