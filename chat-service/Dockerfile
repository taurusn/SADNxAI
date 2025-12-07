FROM python:3.11-slim

WORKDIR /app

# Copy shared module
COPY shared /app/shared

# Copy service files
COPY chat-service/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY chat-service/ .

# Create storage directories
RUN mkdir -p /storage/input /storage/staging /storage/output /storage/reports

ENV STORAGE_PATH=/storage
ENV REDIS_URL=redis://redis:6379/0
ENV MASKING_SERVICE_URL=http://masking-service:8001
ENV VALIDATION_SERVICE_URL=http://validation-service:8002

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
