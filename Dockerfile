# Dockerfile

# Use the official Python 3.10 slim image as the base image
FROM python:3.10-slim

# Set environment variables to prevent Python from writing .pyc files and to ensure that stdout and stderr are sent straight to terminal (e.g. a container log)
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Copy requirements.txt file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code to the container
COPY . .

# Create a non-root user to run the application
RUN useradd -m user
USER user

# Add a health check to monitor the health of the application
HEALTHCHECK --interval=30s --timeout=3s CMD curl -f http://localhost:8000/ || exit 1

# Command to run the application using uvicorn server on port 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]