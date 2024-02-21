# Use an official Python runtime as a parent image
FROM python:3.10-slim
SHELL ["/bin/bash", "-c"]

# Set environment varibles
ENV PYTHONUNBUFFERED=1 \
    # prevents python creating .pyc files
    PYTHONDONTWRITEBYTECODE=1 \
    # pip
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    # poetry
    # https://python-poetry.org/docs/configuration/#using-environment-variables
    POETRY_VERSION=1.7.1 \
    # make poetry install to this location
    POETRY_HOME="/opt/poetry" \
    # make poetry create the virtual environment in the project's root
    # it gets named `.venv`
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    # do not ask any interactive question
    POETRY_NO_INTERACTION=1 \
    VENV_PATH="/opt/pysetup/.venv"

# prepend poetry and venv to path
ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

# Set work directory
WORKDIR /app
COPY models /app/models

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    postgresql-client libpq-dev \
    libpq-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 - --version "$POETRY_VERSION"

# Copy the project files into the container
COPY ["poetry.lock", "pyproject.toml", "/app/"]

# Install project dependencies
RUN poetry install --no-interaction --no-ansi

# Copy the project files into the container
COPY ["llm_logic.py", "app.py", "/app/"]
COPY ["db_scripts/","/app/db_scripts"]
COPY ["dl_scripts", "/app/dl_scripts"]

# Command to run the application
ENV PYTHONPATH=/app:$PYTHONPATH
CMD poetry run streamlit run app.py
