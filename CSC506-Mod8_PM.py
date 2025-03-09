# Importing necessary libraries
import yfinance as yf
import numpy as np
from dtaidistance import dtw
import pandas as pd
import matplotlib.pyplot as plt


def get_user_input():
    """Prompt the user separately for two stock symbols and select a time period."""
    while True:
        stock_1 = input("Enter the first stock symbol: ").strip().upper()
        if stock_1:
            break
        print("Invalid input. Please enter a valid stock symbol.")

    while True:
        stock_2 = input("Enter the second stock symbol: ").strip().upper()
        if stock_2 and stock_2 != stock_1:
            break
        print("Invalid input. Please enter a different valid stock symbol.")

    time_options = {"1": "6mo", "2": "1y", "3": "2y"}
    
    while True:
        print("\nSelect the time period:")
        print("1. 6 months")
        print("2. 1 year")
        print("3. 2 years")
        time_choice = input("Enter the number corresponding to your choice: ").strip()
        
        if time_choice in time_options:
            return stock_1, stock_2, time_options[time_choice]
        
        print("Invalid choice. Please enter 1, 2, or 3.")

def fetch_stock_data(ticker_symbol, period):
    """Fetch historical stock data and return the closing price series."""
    try:
        ticker = yf.Ticker(ticker_symbol)
        data = ticker.history(period=period)
        if data.empty:
            raise ValueError(f"No data found for ticker {ticker_symbol}")
        return data['Close'].fillna(method="ffill").values
    except Exception as e:
        print(f"Error fetching data for {ticker_symbol}: {e}")
        return None

def compute_dtw(series_1, series_2, method="DTW", window=None, downsample_factor=2):
    """Compute DTW distance with optional downsampling or constraints."""
    try:
        if method == "DTW":
            return dtw.distance(series_1, series_2)
        
        elif method == "MDTW":  
            # Adaptive downsampling using a moving average
            downsampled_1 = pd.Series(series_1).rolling(window=downsample_factor).mean().dropna().values
            downsampled_2 = pd.Series(series_2).rolling(window=downsample_factor).mean().dropna().values
            return dtw.distance(downsampled_1, downsampled_2)
        
        elif method == "CDTW":  
            # Dynamic window selection: 10% of series length or user-defined
            adaptive_window = max(5, int(len(series_1) * 0.1)) if window is None else window
            return dtw.distance(series_1, series_2, window=adaptive_window)
    
    except Exception as e:
        print(f"Error computing {method} distance: {e}")
        return None
    
def compute_normalized_dtw(series_1, series_2):
    """Compute normalized DTW distance between two time series."""
    try:
        normalized_dtw = compute_dtw(series_1, series_2)
        if normalized_dtw is None:
            return None
        return normalized_dtw / len(series_1)  # Normalize by series length
    except Exception as e:
        print(f"Error computing normalized DTW: {e}")
        return None


def plot_stock_data(dates, series_1, series_2, label_1, label_2):
    """Plot stock prices of two companies."""
    plt.figure(figsize=(10, 6))
    plt.plot(dates, series_1, label=label_1, color="blue")
    plt.plot(dates, series_2, label=label_2, color="green")
    plt.title(f"Stock Price Comparison: {label_1} vs {label_2}")
    plt.xlabel("Date")
    plt.ylabel("Closing Price (USD)")
    plt.legend()
    plt.show()

# Get user input
stock_1, stock_2, period = get_user_input()

# Fetch data for user-selected stocks
series_1 = fetch_stock_data(stock_1, period)
series_2 = fetch_stock_data(stock_2, period)

if series_1 is not None and series_2 is not None:
    # Ensure both series have equal length
    min_length = min(len(series_1), len(series_2))
    series_1, series_2 = series_1[:min_length], series_2[:min_length]

    # Compute DTW distances
    dtw_dist = compute_dtw(series_1, series_2, method="DTW")
    mdtw_dist = compute_dtw(series_1, series_2, method="MDTW")
    cdtw_dist = compute_dtw(series_1, series_2, method="CDTW")

    # Compute normalized DTW distance
    normalized_dtw = compute_normalized_dtw(series_1, series_2)

    # Print results
    print(f"\nComparing {stock_1} and {stock_2} over {period}:")
    print(f"DTW Distance: {dtw_dist:.2f}")
    print(f"MDTW Distance (Downsampled): {mdtw_dist:.2f}")
    print(f"CDTW Distance (Constrained): {cdtw_dist:.2f}")
    print(f"Normalized DTW Distance: {normalized_dtw:.4f}")

    # Visualization
    dates = pd.date_range(end=pd.Timestamp.today(), periods=min_length)
    plot_stock_data(dates, series_1, series_2, label_1=stock_1, label_2=stock_2)