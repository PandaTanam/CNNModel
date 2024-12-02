FROM python:3.12 AS base

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose the port
EXPOSE 8080 

# Use gunicorn for production, binding to the correct port
CMD ["gunicorn", "-b", ":8080", "app:app"]
