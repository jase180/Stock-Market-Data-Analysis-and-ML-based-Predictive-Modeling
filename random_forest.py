import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import classification_report, confusion_matrix, ConfusionMatrixDisplay
import seaborn as sns
import matplotlib.pyplot as plt
import joblib

#Load data
print("Loading data")
data_path = "data/spy_data_cleaned.csv"
df = pd.read_csv(data_path, encoding='latin1') #need to have the encoding or it will have some window error

#Target creation
df["target"] = (df["close"] > df["open"]).astype(int) # close is higher than open meaning profit

# Drop rows with missing values
df.dropna(inplace=True)

#Features
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
X = df[features]
y = df["target"]

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
joblib.dump(rf_model, 'model1')

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
