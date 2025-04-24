import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# Quarterly weight changes (add more as needed)
quarterly_weights = {
    "2018-01-01": {
        "PERSISTENT.NS": 0.0235,
        "TATAELXSI.NS": 0.0235,
        "HEROMOTOCO.NS": 0.0235,
        "MARUTI.NS": 0.0235,
        "DRREDDY.NS": 0.0278,
        "APOLLOHOSP.NS": 0.0278,
        "DIVISLAB.NS": 0.0321,
        "CIPLA.NS": 0.0321,
        "BRITANNIA.NS": 0.0364,
        "TATACONSUM.NS": 0.0407,
        "BAJAJ-AUTO.NS": 0.0450,
        "TECHM.NS": 0.0450,
        "ULTRACEMCO.NS": 0.0493,
        "HCLTECH.NS": 0.0535,
        "NESTLEIND.NS": 0.0535,
        "WIPRO.NS": 0.0578,
        "SUNPHARMA.NS": 0.0707,
        "ASIANPAINT.NS": 0.0750,
        "INFY.NS": 0.0836,
        "HINDUNILVR.NS": 0.0879,
        "TCS.NS": 0.0879
    }
    # Add more quarters as needed
}

start_date = "2010-01-01"  # Allow earlier start
end_date = "2024-12-31"

# Collect all tickers
all_tickers = set()
for wt in quarterly_weights.values():
    all_tickers.update(wt.keys())
all_tickers.update(["^GSPC", "^NSEI"])

# Download data
data = yf.download(list(all_tickers), start=start_date, end=end_date)["Close"]
data = data.dropna()

# Normalize
normalized = data / data.iloc[0]

# Composite series
composite = pd.Series(index=normalized.index, dtype=float)

# Sort quarters
sorted_quarters = sorted((pd.to_datetime(k), v) for k, v in quarterly_weights.items())

# Assign earliest weights to all dates before the first group
first_date, first_weights = sorted_quarters[0]
mask = normalized.index < first_date
if mask.any():
    temp_data = normalized.loc[mask, first_weights.keys()]
    composite.loc[mask] = (temp_data * pd.Series(first_weights)).sum(axis=1)

# Continue with defined quarters
for i, (start, weights) in enumerate(sorted_quarters):
    end = sorted_quarters[i + 1][0] if i + 1 < len(sorted_quarters) else normalized.index[-1]
    mask = (normalized.index >= start) & (normalized.index <= end)
    temp_data = normalized.loc[mask, weights.keys()]
    composite.loc[mask] = (temp_data * pd.Series(weights)).sum(axis=1)

# Add S&P 500 and Nifty
normalized["S&P 500"] = normalized["^GSPC"]
normalized["Nifty 50"] = normalized["^NSEI"]
normalized.drop(columns=["^GSPC", "^NSEI"], inplace=True)

# Plot
plt.figure(figsize=(14, 7))
plt.plot(composite, label="Hafzan Composite", linewidth=2.5)
plt.plot(normalized["S&P 500"], label="S&P 500", linewidth=1.5)
plt.plot(normalized["Nifty 50"], label="Nifty 50", linewidth=1.5)
plt.title("Hafzan Composite vs S&P 500 and Nifty 50")
plt.xlabel("Date")
plt.ylabel("Normalized Value")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
