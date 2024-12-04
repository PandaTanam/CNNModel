# Use a specific version of Python for consistency
FROM python:3.9

# Set the working directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install -r requirements.txt

# Copy application code
COPY . .

# Expose the port that the app runs on
EXPOSE 8080 

# Command to run the application using Gunicorn with Uvicorn workers
CMD ["gunicorn", "main:app", "-b", "0.0.0.0:8080"]