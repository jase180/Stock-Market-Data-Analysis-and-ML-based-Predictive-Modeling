import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import classification_report, confusion_matrix, ConfusionMatrixDisplay
import seaborn as sns
import matplotlib.pyplot as plt
import joblib

#Load data  #CHANGE THE DATA PATH LOADING
print("Loading data")
data_path_features = "data/spy_data_cleaned_premarket.pk1"
data_path_target = "data/spy_data_cleaned_close.pk1"

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
features = [
    "momentum_rsi",
    "momentum_stoch_rsi",
    "momentum_stoch_rsi_k",
    "momentum_stoch_rsi_d",
    "trend_macd",
    "trend_macd_signal",
    "trend_macd_diff",
    "volume_sma_em",
    "trend_sma_fast",
    "trend_sma_slow"
]
X = df_features[features]
y = df_features["target"]
print(f"shapes: X: {X.shape}, y: {y.shape}")

#Split Test-train data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

#Use Scaler
scaler = MinMaxScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

#Rainforest here we goooo
print("ML Here we go!")
rf_model = RandomForestClassifier(n_estimators=500, random_state=42)
rf_model.fit(X_train_scaled, y_train)

#Save the model
print("Done and saving!")
joblib.dump(rf_model, 'model1.pk1')

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
plt.barh(features,importance)
plt.xlabel('Importance')
plt.ylabel('Features')
plt.show()
