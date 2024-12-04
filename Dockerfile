# Use a specific version of Python for consistency
FROM python:3.12-slim AS base

# Set the working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose the port that the app runs on
EXPOSE 8080 

# Command to run the application
CMD ["uvicorn", "-b", ":8080", "main:app"]