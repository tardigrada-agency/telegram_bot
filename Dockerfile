FROM python:3.10.0rc1-slim-bullseye

RUN mkdir app


RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y libghc-zlib-dev libpq-dev gcc && \
    apt-get clean

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD python main.py

