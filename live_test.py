import requests
import pandas as pd
import time


#Polygon API info for getting live info
api_key = "CP7pXlsPyynAOZbpAqB8OX98ANuOG4Os"
url = "https://api.polygon.io/v2/aggs/ticker/SPY/range/1/minute/2024-11-02/2024-11-26?adjusted=true&sort=asc&limit=50000&apiKey=CP7pXlsPyynAOZbpAqB8OX98ANuOG4Os"

#portfolio (declare variables for the paper trading)

portfolio = {"cash":10000, "SPY shares":0}
trade_log = []

def fetch_live_data_from_polygon(ticker):
    return data

def preprocess_live_data_from_polygon(data):
    return data

def predict(data, model):
    pass
    return decision

def paper_trade(decision):
    pass

if __name__=="__main__":
    try:
        data = fetch_live_data_from_polygon('SPY')
        print("fetched SPY data")

        data = preprocess_live_data_from_polygon(data)
        print("data preprocessed")

        decision = predict(data, model)

        paper_trade(decision)
    except Exception as e:
        print(f"Error: {e}")

