FROM python:3.10-slim-buster

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /app

COPY . /app

RUN groupadd -r appgroup && useradd -r -g appgroup -m -s /bin/bash appuser
RUN chown -R appuser:appgroup /app

USER appuser

# Gunakan gunicorn dengan argumen yang lebih aman
CMD ["gunicorn", "--bind", "0.0.0.0:9000", "--workers", "3", "--threads", "2", "app:app"]
