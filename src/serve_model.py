import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import numpy as np
import onnxruntime as ort
import pickle
import logging
import sys

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)

# Paths
ENCODER_DIR = "./encoders"
ONNX_MODEL_PATH = "models/model.onnx"

# Load ONNX model
session = ort.InferenceSession(ONNX_MODEL_PATH, providers=["CPUExecutionProvider"])
input_name = session.get_inputs()[0].name
output_name = session.get_outputs()[0].name

logging.info("ONNX model loaded.")

# Load saved encoders
categorical_cols = ["hypertension", "heart_disease", "gender", "smoking_history"]
encoders = {}

for col in categorical_cols:
    with open(f"{ENCODER_DIR}/{col}_encoder.pkl", "rb") as f:
        encoders[col] = pickle.load(f)

logging.info("Encoders loaded successfully.")

feature_columns = ['gender', 'age', 'hypertension', 'heart_disease', 'smoking_history', 'bmi', 'HbA1c_level', 'blood_glucose_level']

# FastAPI setup
app = FastAPI(
    title="Diabetes Prediction API",
    description="Predict diabetes using ONNX runtime with original training encoders",
    version="1.0"
)

class InputData(BaseModel):
    data: dict


@app.get("/")
def root():
    logging.info("Received GET request at /")
    return {"status": "API is running"}


@app.post("/predict")
def predict(payload: InputData):
    logging.info("Received POST request at /predict")
    raw = payload.data

    # Convert raw to dataframe
    df = pd.DataFrame([raw])

    # Apply saved label encoders
    for col in categorical_cols:
        if col in df.columns:
            val = df[col].iloc[0]

            # Prevent unknown categories
            if val not in encoders[col].classes_:
                logging.error(f"Unknown category {val} encountered for column {col}")
                return {
                    "error": f"Unknown category '{val}' for column '{col}'. "
                             f"Allowed: {list(encoders[col].classes_)}"
                }

            df[col] = encoders[col].transform(df[col])

    # Ensure correct column order
    df = df.reindex(columns=feature_columns)

    # Convert to float32
    input_array = df.values.astype(np.float32)

    # ONNX inference
    result = session.run([output_name], {input_name: input_array})
    prediction = int(result[0][0])

    logging.info(f"Prediction: {prediction}")

    return {
        "prediction": prediction,
        "processed_input": df.iloc[0].to_dict()
    }


if __name__ == "__main__":
    logging.info("Starting server...")
    uvicorn.run("serve_model:app", host="0.0.0.0", port=8000)