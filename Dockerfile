#--------------------------------------------------------------------
# DockerFile used to setup the environment when deploying to Railway
#--------------------------------------------------------------------

# Use the official Python image from the Docker Hub
FROM python:3-slim

# Set the working directory in the container
WORKDIR /app

# Copy application code into the container
COPY . .

# Install packages
RUN pip install -r ./requirements.txt

