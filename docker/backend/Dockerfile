FROM python:3.12
LABEL authors="dima.sichkar2003@gmail.com"

ENV PYTHONUNBUFFERED=1

RUN apt update && apt install -y dos2unix #Install necessary packages and convert Windows-style line endings (CRLF) to Unix-style (LF).

#RUN pip install --no-cache-dir -r requirements.txt # запобігає збереженню кешу встановлених пакетів, що може зменшити розмір контейнера. Поки не використовую, залишив для фінальної збірки з Alpine образом
RUN pip install --upgrade pip
#RUN pip install gunicorn --> will be needed for multithreading

# Встановлюємо Poetry
ENV POETRY_VERSION=2.1.1
RUN curl -sSL https://install.python-poetry.org | python3 -

# Додаємо Poetry до змінної PATH
ENV PATH="/root/.local/bin:$PATH"

# Встановлюємо налаштування Poetry (використовуємо системний інтерпретатор без віртуального середовища)
RUN poetry config virtualenvs.create false

# Створюємо робочу директорію
WORKDIR /app

# Копіюємо файли проєкту (важливо, щоб спочатку копіювалися лише файли залежностей)
COPY pyproject.toml poetry.lock ./

# Встановлюємо залежності через Poetry
RUN poetry install --no-root --no-interaction --no-ansi

ADD ./src /app/backend
ADD ./docker /app/docker
