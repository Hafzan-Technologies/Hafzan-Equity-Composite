import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# Example stock list (Feel free to modify)
stocks = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA']

# Example date range
start_date = '2023-01-01'
end_date = '2024-01-01'

# Function to get stock data
def get_stock_data(stocks, start, end):
    data = pd.DataFrame()
    for stock in stocks:
        print(f"Downloading data for {stock}...")
        df = yf.download(stock, start=start, end=end)
        if not df.empty and 'Close' in df.columns:
            data[stock] = df['Close']
        else:
            print(f"⚠️ Warning: No valid 'Close' price data for {stock}")
    return data

# Function to create composite index and plot
def create_and_plot_index(start, end):
    stock_data = get_stock_data(stocks, start, end)

    if stock_data.empty:
        print("❌ No data downloaded. Exiting.")
        return

    # Normalize all stock prices to start at 100
    normalized_data = stock_data / stock_data.iloc[0] * 100

    # Calculate average to form composite index
    composite_index = normalized_data.mean(axis=1)

    # Plotting
    plt.figure(figsize=(12, 6))
    plt.plot(composite_index, label='📈 Hafzan Composite Index', color='green', linewidth=2)
    plt.title('Hafzan Composite Index (2023)', fontsize=16)
    plt.xlabel('Date')
    plt.ylabel('Index Value (Base = 100)')
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

# Run the function
create_and_plot_index(start_date, end_date)
