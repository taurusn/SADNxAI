FROM python:3.11-slim

WORKDIR /app

# Copy shared module
COPY shared /app/shared

# Copy service files
COPY masking-service/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY masking-service/ .

# Create storage directories
RUN mkdir -p /storage/input /storage/staging /storage/output /storage/reports

ENV STORAGE_PATH=/storage

EXPOSE 8001

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]
