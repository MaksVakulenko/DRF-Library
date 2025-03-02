FROM python:3.12
LABEL authors="dima.sichkar2003@gmail.com"

ENV PYTHONUNBUFFERED=1

RUN apt update && apt install -y dos2unix #Install necessary packages and convert Windows-style line endings (CRLF) to Unix-style (LF).

#RUN pip install --no-cache-dir -r requirements.txt # запобігає збереженню кешу встановлених пакетів, що може зменшити розмір контейнера. Поки не використовую, залишив для фінальної збірки з Alpine образом
RUN pip install --upgrade pip
#RUN pip install gunicorn --> will be needed for multithreading
ADD ./requirements.txt /app/
RUN pip install -r /app/requirements.txt

ADD ./src /app/backend
ADD ./docker /app/docker
