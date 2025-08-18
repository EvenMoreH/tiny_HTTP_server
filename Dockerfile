# Use official Python image (3.12 or higher)
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Expose port 8000 (change if your server uses a different port)
EXPOSE 5073

# Run the server
CMD ["python", "server.py"]
