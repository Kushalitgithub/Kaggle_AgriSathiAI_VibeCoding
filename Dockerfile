# Use official lightweight Python image
FROM python:3.12-slim

# Set working directory inside container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install python packages
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy all project source code
COPY . .

# Seed the database inside the container
RUN python database/seed_db.py

# Expose Streamlit default port
EXPOSE 8501

# Configure Streamlit health checks
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Run the Streamlit dashboard on startup
ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
