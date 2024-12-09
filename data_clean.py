import pandas as pd
from ta import add_all_ta_features
import os

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

#RESAMPLING for 1 day
df_daily = df.resample("1D").agg({
    "Open": "first",   # First price of the day
    "High": "max",     # Highest price of the day
    "Low": "min",      # Lowest price of the day
    "Close": "last",   # Last price of the day
    "Volume": "sum"    # Total volume of the day
})

print("Daily resampled data:")
print(df_daily.head(10))

#rename columns to lowercase so it works with TA
df.rename(columns={
    "Open": "open",
    "High": "high",
    "Low": "low",
    "Close": "close",
    "Volume": "volume"
}, inplace=True)
print("columns name check:",df.columns)

#TA Calculations

df = add_all_ta_features(
    df,
    open="open",
    high="high",
    low="low",
    close="close",
    volume="volume",
    fillna=True  # Fill missing values in indicators
)
print("checking after TA add")
print(df.head(10)) 

# extract premarket and first 30 minutes data
df_premarket = df.between_time('10:00','10:00')

#extract daily close
df_close = df.between_time('16:00', '16:00')

#export to df
print("To pickling the dfs")
df_premarket.to_pickle("data/spy_data_cleaned_premarket.pk1")
df_close.to_pickle("data/spy_data_cleaned_close.pk1")

#Done and write to csv
print("Done and now write to csv...")
output_path = "data/spy_data_cleaned.csv"
df.to_csv(output_path)

df_premarket.to_csv("data/spy_data_cleaned_premarket.csv")
df_close.to_csv("data/spy_data_cleaned_close.csv")
