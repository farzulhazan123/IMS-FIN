# Use an official Python runtime as the base image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /app

# Copy requirements.txt
COPY requirements.txt .

# Install dependencies
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code into the container
COPY . .

# Expose the port
EXPOSE 5000

# Set permissions to allow SQLite to write
RUN chmod -R 777 /app

# Run Flask app
CMD ["python", "app.py"]
