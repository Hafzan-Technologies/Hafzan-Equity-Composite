import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# Example stock list for Hafzan Composite
stocks = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA']

# Date range
start_date = '2023-01-01'
end_date = '2024-01-01'

# Function to get and normalize stock data
def get_normalized_data(tickers, start, end, label):
    data = pd.DataFrame()
    for ticker in tickers:
        print(f"Downloading data for {ticker}...")
        df = yf.download(ticker, start=start, end=end)
        if not df.empty and 'Close' in df.columns:
            data[ticker] = df['Close']
        else:
            print(f"⚠️ Warning: No valid 'Close' price data for {ticker}")
    
    # Normalize
    normalized = data / data.iloc[0] * 100
    if len(tickers) > 1:
        index = normalized.mean(axis=1)
        index.name = label
    else:
        index = normalized[tickers[0]]
        index.name = label
    return index

# Main function to plot everything
def create_and_compare_indexes(start, end):
    hafzan_index = get_normalized_data(stocks, start, end, 'Hafzan Composite Index')
    sp500_index = get_normalized_data(['^GSPC'], start, end, 'S&P 500')
    nifty50_index = get_normalized_data(['^NSEI'], start, end, 'Nifty 50')

    # Combine all indices
    combined = pd.concat([hafzan_index, sp500_index, nifty50_index], axis=1)

    # Plotting
    plt.figure(figsize=(14, 7))
    plt.plot(combined, linewidth=2)
    plt.title('📊 Hafzan Composite vs S&P 500 vs Nifty 50 (2023)', fontsize=16)
    plt.xlabel('Date')
    plt.ylabel('Normalized Index Value (Base = 100)')
    plt.grid(True)
    plt.legend(combined.columns)
    plt.tight_layout()
    plt.show()

# Run
create_and_compare_indexes(start_date, end_date)
