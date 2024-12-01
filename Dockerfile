FROM python:3.10-slim AS base

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose the port
EXPOSE 8080

# Use gunicorn for production
CMD ["gunicorn", "-b", "0.0.0.0:9000", "app:app"]
