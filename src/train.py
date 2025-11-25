import pandas as pd
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score
import mlflow
import mlflow.sklearn
import os

import onnxmltools
from onnxmltools.convert.common.data_types import FloatTensorType

TRAINING_DATASET_PATH = "./processed_data/train.csv"
RANDOM_SEED = 100

train_df = pd.read_csv(TRAINING_DATASET_PATH)

## Separate features and target
y_train = train_df["diabetes"]
X_train = train_df.drop("diabetes", axis=1)

n_features = X_train.shape[1]
initial_type = [('float_input', FloatTensorType([None, n_features]))]

mlflow.set_tracking_uri("sqlite:///mlflow.db")

with mlflow.start_run():

    xgb_model = XGBClassifier(random_state=RANDOM_SEED)
    xgb_model.fit(X_train, y_train)

    preds = xgb_model.predict(X_train)
    accuracy = accuracy_score(y_train, preds)

    mlflow.log_metric("training_accuracy", accuracy)
    mlflow.log_param("model", "XGBoost")

    # Log full training model
    mlflow.sklearn.log_model(xgb_model, "training_model")

    booster = xgb_model.get_booster()
    booster.feature_names = None

    # Convert XGB model to ONNX
    onnx_model = onnxmltools.convert_xgboost(xgb_model, initial_types=initial_type)

    os.makedirs("models", exist_ok=True)
    onnx_path = "models/model.onnx"
    with open(onnx_path, "wb") as f:
        f.write(onnx_model.SerializeToString())

    # Log ONNX as artifact for deployment
    mlflow.log_artifact(onnx_path)

    print(f"Training complete. Accuracy Score: {accuracy}")
    print("XGBoost model trained and saved successfully.")