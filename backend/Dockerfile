# Use a slim official Python image (memory & size friendly)
FROM python:3.11-slim

# Set working dir inside container
WORKDIR /app

# Prevent Python from writing .pyc files and enable stdout/stderr buffering
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Install system deps required for some packages (if needed)
# (kept minimal to reduce image size)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy only requirements first for cached layer installation
COPY requirements.txt .

# Install python deps (use pip, upgrade pip first)
RUN python -m pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .
RUN chown -R 1000:1000 /app

# Expose the port the app will run on
EXPOSE 8000

# Use non-root user for better security (optional)
RUN groupadd -g 1000 appuser && useradd -r -u 1000 -g appuser appuser
USER appuser

# Default command to run the app. We'll use uvicorn.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

