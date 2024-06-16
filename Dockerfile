FROM python:3.9-slim

RUN apt-get update && \
    apt-get install -y \
    iputils-ping && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . .

ENTRYPOINT ["python", "main.py"]
