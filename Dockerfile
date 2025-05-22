# Use an official Python runtime as a parent image
FROM python:3.11-slim

RUN apt-get update && apt-get install -y curl && \
    curl -sSL https://github.com/jwilder/dockerize/releases/download/v0.6.1/dockerize-linux-amd64-v0.6.1.tar.gz | tar -xz -C /usr/local/bin


# Set the working directory in the container
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app/

# Expose the port FastAPI will run on
EXPOSE 8000

# Command to run the FastAPI app using Uvicorn
CMD /bin/bash -c "export PYTHONPATH=/app && dockerize -wait tcp://kafka:9092 -timeout 60s && python3 /app/app/infrastructure/consumer.py & uvicorn main:app --host 0.0.0.0 --port 8000 --reload"
