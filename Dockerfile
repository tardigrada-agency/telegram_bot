FROM python:3.10.0rc1-slim-bullseye

RUN mkdir app

WORKDIR /app

COPY . .

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y libghc-zlib-dev libpq-dev gcc && \
    apt-get clean
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

CMD python main.py

