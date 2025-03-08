# Importing necessary libraries
import yfinance as yf
import numpy as np
from dtaidistance import dtw
import pandas as pd
import matplotlib.pyplot as plt

def fetch_stock_data(ticker_symbol, period="1y"):
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

def compute_dtw(series_1, series_2, method="DTW", window=None):
    """Compute DTW distance between two time series."""
    try:
        if method == "DTW":
            return dtw.distance(series_1, series_2)
        elif method == "MDTW":  # Downsampled DTW
            return dtw.distance(series_1[::2], series_2[::2])
        elif method == "CDTW":  # Constrained DTW
            return dtw.distance(series_1, series_2, window=window)
    except Exception as e:
        print(f"Error computing {method} distance: {e}")
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

# Fetch data for Ford (F) and General Motors (GM)
series_1 = fetch_stock_data("F")
series_2 = fetch_stock_data("GM")

if series_1 is not None and series_2 is not None:
    # Ensure both series have equal length
    min_length = min(len(series_1), len(series_2))
    series_1, series_2 = series_1[:min_length], series_2[:min_length]

    # Compute DTW distances
    dtw_dist = compute_dtw(series_1, series_2, method="DTW")
    mdtw_dist = compute_dtw(series_1, series_2, method="MDTW")
    cdtw_dist = compute_dtw(series_1, series_2, method="CDTW", window=10)

    # Print results
    print(f"DTW Distance: {dtw_dist:.2f}")
    print(f"MDTW Distance (Downsampled): {mdtw_dist:.2f}")
    print(f"CDTW Distance (Constrained, window=10): {cdtw_dist:.2f}")

    # Visualization
    dates = pd.date_range(end=pd.Timestamp.today(), periods=min_length)
    plot_stock_data(dates, series_1, series_2, label_1="F", label_2="GM")
