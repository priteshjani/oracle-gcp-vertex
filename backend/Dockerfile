# Use official Python image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies for Oracle Client (if needed for Thick mode)
# For Thin mode (python-oracledb default), basic libs are usually enough.
# Below 3 commented as per Gemini
#RUN apt-get update && apt-get install -y --no-install-recommends \
#    libaio1 \
#    && rm -rf /var/lib/apt/lists/*

RUN apt-get update && apt-get install -y --no-install-recommends libaio1 phython3-dev gcc  || apt-get install -y --no-install-recommends libaio1t64 && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 8080

# Command to run the application
# Use 0.0.0.0 for Cloud Run
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
