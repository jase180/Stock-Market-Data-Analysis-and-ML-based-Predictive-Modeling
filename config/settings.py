"""
Configuration settings for the stock data grabber project.
"""
import os
from pathlib import Path

# Project root directory
PROJECT_ROOT = Path(__file__).parent.parent

# Data paths
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_PATH = DATA_DIR / "spy_data.csv"
PROCESSED_FEATURES_PATH = DATA_DIR / "spy_data_cleaned_premarket.pk1"
PROCESSED_TARGET_PATH = DATA_DIR / "spy_data_cleaned_close.pk1"

# Model paths
MODELS_DIR = PROJECT_ROOT / "models"
MODEL_PATH = MODELS_DIR / "random_forest_model.pkl"

# API settings
POLYGON_API_KEY = os.getenv("POLYGON_API_KEY")
BASE_URL = "https://api.polygon.io/v2/aggs/ticker"

# Data collection date range
# Note: Due to Polygon's limit of 50,000 records per request,
# collect data in 2-month chunks to avoid hitting the limit
DATA_START_DATE = "2025-09-01"
DATA_END_DATE = "2025-09-23"

# Model parameters
RANDOM_FOREST_PARAMS = {
    "n_estimators": 10000,
    "random_state": 42
}

# Feature columns for ML model
FEATURE_COLUMNS = [
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

# Trading parameters
INITIAL_CASH = 10000
TEST_SIZE = 0.2