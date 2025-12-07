FROM python:3.11-slim

WORKDIR /app

# Copy shared module
COPY shared /app/shared

# Copy service files
COPY validation-service/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY validation-service/ .

# Create storage directories
RUN mkdir -p /storage/input /storage/staging /storage/output /storage/reports

ENV STORAGE_PATH=/storage

EXPOSE 8002

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8002"]
