# Use the official Python image from the Docker Hub
FROM python:3.12

ENV PYTHONUNBUFFERED True

ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port that the app runs on
ENV PORT 8080

# Command to run the application
CMD ["gunicorn", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "main:app", "--bind", "0.0.0.0:8080", "--preload"]