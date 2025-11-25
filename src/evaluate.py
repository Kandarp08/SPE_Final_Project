import json
import mlflow
import pandas as pd
import onnxruntime as ort
from sklearn.metrics import accuracy_score

VAL_DATASET_PATH = "./processed_data/val.csv"

val_df = pd.read_csv(VAL_DATASET_PATH)
X = val_df.drop("diabetes", axis=1)
y = val_df["diabetes"]

# Load the candidate ONNX model
session = ort.InferenceSession("models/model.onnx")
input_name = session.get_inputs()[0].name
preds = session.run(None, {input_name: X.astype("float32").values})[0]

accuracy = accuracy_score(y, preds)

print(f"Model accuracy on validation data: {accuracy}")

# Save metrics — tracked by DVC
json.dump({"validation_accuracy": accuracy}, open("metrics.json", "w"))
