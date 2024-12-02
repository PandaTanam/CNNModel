FROM python:3.12 AS base

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose the port
EXPOSE 9000 

# Use gunicorn for production, binding to the correct port
CMD ["gunicorn", "-b", "0.0.0.0:9000", "app:app"]
