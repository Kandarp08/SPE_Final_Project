FROM python:3.10-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r container_requirements.txt

# Copy model + encoders + data + API script
COPY serve_model.py .
COPY models/ models/
COPY encoders/ encoders/

EXPOSE 8000

CMD ["python", "serve_model.py"]