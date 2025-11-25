import pandas as pd
from sklearn.preprocessing import OneHotEncoder, LabelEncoder
from sklearn.model_selection import train_test_split
from imblearn.over_sampling import SMOTE
import os

DATASET_PATH = "./data/diabetes_prediction_dataset_2.csv"
PROCESSED_DATA_DIR = "./processed_data"
TEST_RATIO = 0.2
RANDOM_SEED = 100

df = pd.read_csv(DATASET_PATH)

#Perform label encoding for now
categorical_cols = ['hypertension', 'heart_disease', 'gender', 'smoking_history']

for col in categorical_cols:
    if col in df.columns:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col])

## Separate features and target
y = df['diabetes']
X = df.drop('diabetes', axis=1)

##test train split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=TEST_RATIO, random_state=RANDOM_SEED, stratify=y)

#Using SMOTE function (Since No. of people not having diabetes is much higher than the ones having it)
#SMOTE should only be applied on the training data (to make sure model doesn't predict always 0 or always 1)
#It shouldn't be applied on the test data, bcoz there you just want to check the actual result
smote = SMOTE(random_state=RANDOM_SEED)
X_train_balanced, y_train_balanced = smote.fit_resample(X_train, y_train)

if not os.path.exists(PROCESSED_DATA_DIR):
    os.makedirs(PROCESSED_DATA_DIR)

# Combine balanced training features and labels
train_df = pd.concat([pd.DataFrame(X_train_balanced), 
                      pd.Series(y_train_balanced, name="diabetes")], axis=1)

# Combine test features and labels
test_df = pd.concat([pd.DataFrame(X_test), 
                     pd.Series(y_test, name="diabetes")], axis=1)

# Save to CSV
train_df.to_csv(os.path.join(PROCESSED_DATA_DIR, "train.csv"), index=False)
test_df.to_csv(os.path.join(PROCESSED_DATA_DIR, "val.csv"), index=False)

print("train.csv and test.csv saved successfully.")