# Use a specific version of Python for consistency
FROM python:3.12 AS base

# Set the working directory
WORKDIR /app

# Set environment variables for the application
ENV PORT 8080
ENV HOST 0.0.0.0

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose the port that the app runs on
EXPOSE 8080 

# Health check to ensure the app is running
HEALTHCHECK CMD curl --fail http://localhost:$PORT/ || exit 1

# Use Uvicorn for production, binding to the correct host and port
CMD ["sh", "-c", "uvicorn app:app --host $HOST --port $PORT"]