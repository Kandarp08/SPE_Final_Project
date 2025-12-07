FROM python:3.10-slim

WORKDIR /app

# Install dependencies
COPY container_requirements.txt .
RUN pip install --no-cache-dir -r container_requirements.txt

# Copy API script, model, and encoders
COPY src/serve_model.py .
COPY models/model.onnx models/model.onnx
COPY encoders/ encoders/

EXPOSE 8000

CMD ["python", "serve_model.py"]