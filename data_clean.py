import pandas as pd
import numpy as np
from ta import add_all_ta_features

data_path = "data/spy_data.csv" #path of the csv file
df = pd.read_csv(data_path) #read the csv into a df

#CLEANING
df["timestamp"] = pd.to_datetime(df["timestamp"], errors='coerce', utc=True) #Convert datetime to pandas datetime
df["timestamp"] = df["timestamp"].dt.tz_convert("US/Eastern").dt.tz_localize(None) #Remove the timezone (UTC -5) and set to USEast

invalid_rows = df[df["timestamp"].isna()]

print(df["timestamp"].head(10))

print("Invalid rows that were dropped:")
print(invalid_rows)

df.set_index("timestamp", inplace = True) #Make datetime into the index of the df

print(f"Index type: {type(df.index)}") 

#RESAMPLING
df_daily = df.resample("1D").agg({
    "Open": "first",   # First price of the day
    "High": "max",     # Highest price of the day
    "Low": "min",      # Lowest price of the day
    "Close": "last",   # Last price of the day
    "Volume": "sum"    # Total volume of the day
})

print(df.loc["2022-12-03"])


print("Daily resampled data:")
print(df_daily.head(10))