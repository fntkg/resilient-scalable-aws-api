# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy requirements file and install dependencies
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY main.py main.py

# Expose the port the app runs on
EXPOSE 80

# Define the command to run the application
CMD ["python", "main.py"]
