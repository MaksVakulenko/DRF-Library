FROM python:3.12
LABEL authors="dima.sichkar2003@gmail.com"

ENV PYTHONUNBUFFERED=1

RUN apt update && apt install -y dos2unix #Install necessary packages and convert Windows-style line endings (CRLF) to Unix-style (LF).

#RUN pip install --no-cache-dir -r requirements.txt # prevents saving the cache of installed packages, which can reduce the size of the container. Not using it yet, left for the final build with the Alpine image
RUN pip install --upgrade pip
#RUN pip install gunicorn --> will be needed for multithreading

# Install Poetry
ENV POETRY_VERSION=2.1.1
RUN curl -sSL https://install.python-poetry.org | python3 -

# Add Poetry to the PATH variable
ENV PATH="/root/.local/bin:$PATH"

# Setting up Poetry (using the system interpreter without a virtual environment)
RUN poetry config virtualenvs.create false

# Create working directory
WORKDIR /app

# Copy the project files (it is important that only the dependency files are copied first)
COPY pyproject.toml poetry.lock ./

# Setting dependencies through Poetry
RUN poetry install --no-root --no-interaction --no-ansi

ADD ./src /app/backend
ADD ./docker /app/docker
