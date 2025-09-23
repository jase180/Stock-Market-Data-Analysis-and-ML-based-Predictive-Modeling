import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import classification_report, confusion_matrix, ConfusionMatrixDisplay
import seaborn as sns
import matplotlib.pyplot as plt
import joblib
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))

from config.settings import (
    PROCESSED_FEATURES_PATH,
    PROCESSED_TARGET_PATH,
    MODEL_PATH,
    FEATURE_COLUMNS,
    RANDOM_FOREST_PARAMS,
    TEST_SIZE
)

#Load data
print("Loading data")
data_path_features = PROCESSED_FEATURES_PATH
data_path_target = PROCESSED_TARGET_PATH

df_features = pd.read_pickle(data_path_features)
df_target = pd.read_pickle(data_path_target)
print("Data loaded")
print(f"Shape after load features: {df_features.shape}")
print(f"Shape after load target: {df_target.shape}")

#Make sure dfs are aligned by timestamps
print("Converting timestamps to dates for alignment")
df_features.index = df_features.index.normalize()
df_target.index = df_target.index.normalize()

print("Aligning by date")
df_features, df_target = df_features.align(df_target, join="inner", axis=0)

print("check after alignment")
print(f"Shape after load features: {df_features.shape}")
print(f"Shape after load target: {df_target.shape}")

#Target creation
print("Creating target")
df_features["target"] = (df_target["close"] > df_features["open"]).astype(int) # close is higher than open meaning profit
print(f"Created target, checking df_features shape: {df_features.shape}")

# Drop rows with missing values
print("Dropping rows")
df_features.dropna(inplace=True)
print(f"Shape after drop: {df_features.shape}")

#Features
print("Loading features and creating X and Y")
X = df_features[FEATURE_COLUMNS]
y = df_features["target"]
print(f"shapes: X: {X.shape}, y: {y.shape}")

#Split Test-train data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=TEST_SIZE, random_state=42)

#Use Scaler
scaler = MinMaxScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

#Rainforest here we goooo
print("ML Here we go!")
rf_model = RandomForestClassifier(**RANDOM_FOREST_PARAMS)
rf_model.fit(X_train_scaled, y_train)

#Save the model
print("Done and saving!")
joblib.dump(rf_model, MODEL_PATH)

#Predictions
y_pred = rf_model.predict(X_test_scaled)

#Evaluation
print("Confusion Matrix:")
print(confusion_matrix(y_test, y_pred))
print("Classification Report:")
print(classification_report(y_test, y_pred))

#Visualization
print("Visualizing")
ConfusionMatrixDisplay.from_estimator(rf_model, X_test_scaled, y_test) 
report = classification_report(y_test, y_pred, output_dict=True)
sns.heatmap(pd.DataFrame(report).iloc[:-1, :].T, annot=True)

#Feature Importance visual
print("Importance visual")
importance = rf_model.feature_importances_
plt.barh(FEATURE_COLUMNS, importance)
plt.xlabel('Importance')
plt.ylabel('Features')
plt.show()
