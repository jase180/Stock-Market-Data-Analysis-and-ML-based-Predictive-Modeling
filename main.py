import requests
import csv
from datetime import datetime, timedelta

API_KEY = "your_api_key"  # Replace with your API key
TICKER = "SPY"
BASE_URL = "https://api.polygon.io/v2/aggs/ticker"
CSV_FILE = "spy_data.csv"

def fetch_data(start, end):
    endpoint = f"{BASE_URL}/{TICKER}/range/1/minute/{start}/{end}"
    params = {
        "adjusted": "true",
        "sort": "asc",
        "apiKey": API_KEY
    }
    response = requests.get(endpoint, params=params)
    if response.ok:
        return response.json()
    else:
        print(f"Error: Unable to fetch data for {start} to {end} (Status {response.status_code})")
        return None

def create_date_ranges(start_date):
    now = datetime.utcnow()
    ranges = []
    while start_date < now:
        next_month = (start_date + timedelta(days=32)).replace(day=1)
        end_date = next_month - timedelta(days=1)
        if end_date > now:
            end_date = now
        ranges.append((start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d")))
        start_date = next_month
    return ranges

def write_to_csv(data, file_name):
    rows = []
    if "results" in data:
        for entry in data["results"]:
            rows.append([
                datetime.utcfromtimestamp(entry["t"] / 1000).strftime("%Y-%m-%d %H:%M:%S"),
                entry["o"], entry["h"], entry["l"], entry["c"], entry["v"]
            ])
    file_exists = False
    try:
        with open(file_name, "r"):
            file_exists = True
    except FileNotFoundError:
        pass

    with open(file_name, "a", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["timestamp", "open", "high", "low", "close", "volume"])
        writer.writerows(rows)

def main():
    start_date = datetime(2022, 11, 20)
    date_ranges = create_date_ranges(start_date)

    for start, end in date_ranges:
        print(f"Retrieving data from {start} to {end}")
        response = fetch_data(start, end)
        if response:
            print(f"Fetched {len(response.get('results', []))} entries.")
            write_to_csv(response, CSV_FILE)
        else:
            print(f"Skipped {start} to {end} due to an error.")

if __name__ == "__main__":
    main()
