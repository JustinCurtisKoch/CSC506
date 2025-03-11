import yfinance as yf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from dtaidistance import dtw

# Prompt user for stock symbols and a time period
def get_user_input():
    stock_1 = input("Enter the first stock symbol: ").strip().upper()
    stock_2 = input("Enter the second stock symbol: ").strip().upper()
    while stock_1 == stock_2:
        print("Stock symbols must be different.")
        stock_2 = input("Enter a different second stock symbol: ").strip().upper()
    
    time_options = {"1": "6mo", "2": "1y", "3": "2y"}
    while True:
        time_choice = input("\nSelect the time period (1: 6mo, 2: 1y, 3: 2y): ").strip()
        if time_choice in time_options:
            return stock_1, stock_2, time_options[time_choice]
        print("Invalid choice. Enter 1, 2, or 3.")

# Fetch historical stock data and return the closing price series
def fetch_stock_data(ticker_symbol, period):
    try:
        data = yf.Ticker(ticker_symbol).history(period=period)
        if data.empty:
            raise ValueError(f"No data found for {ticker_symbol}")
        return data['Close'].ffill().values
    except Exception as e:
        print(f"Error fetching data for {ticker_symbol}: {e}")
        return None

# Compute tradiotnal DTW distance
# Allows for optional MDTW downsampling or CDTW constraint
def compute_dtw(series_1, series_2, method="DTW", window=None, downsample_factor=2):
    try:
        if method == "MDTW":
            series_1 = pd.Series(series_1).rolling(downsample_factor).mean().dropna().values
            series_2 = pd.Series(series_2).rolling(downsample_factor).mean().dropna().values
        elif method == "CDTW":
            window = window or max(5, int(len(series_1) * 0.1))
        return dtw.distance(series_1, series_2, window=window)
    except Exception as e:
        print(f"Error computing {method} distance: {e}")
        return None

# Compute normalized DTW distance
# Normalizes the DTW distance by the length of the series
def compute_normalized_dtw(series_1, series_2):
    dtw_dist = compute_dtw(series_1, series_2)
    return dtw_dist / len(series_1) if dtw_dist else None

# Plot stock data for visual comparison
def plot_stock_data(series_1, series_2, label_1, label_2):
    plt.figure(figsize=(10, 5))
    plt.plot(series_1, label=label_1, color="blue")
    plt.plot(series_2, label=label_2, color="green")
    plt.title(f"Stock Price Comparison: {label_1} vs {label_2}")
    plt.xlabel("Time")
    plt.ylabel("Closing Price (USD)")
    plt.legend()
    plt.show()

# Generate alternative DTW visualizations
def plot_alternative_dtw_visualizations(series_1, series_2):
    fig, ax = plt.subplots(2, 2, figsize=(14, 10))
    
    # Cumulative DTW Distance
    cumulative_distances = np.cumsum([dtw.distance(series_1[:i], series_2[:i]) for i in range(1, len(series_1))])
    ax[0, 0].plot(cumulative_distances, color="blue")
    ax[0, 0].set_title("Cumulative DTW Distance Over Time")
    
    # Rolling DTW Distance
    rolling_dtw = [dtw.distance(series_1[i:i+30], series_2[i:i+30]) for i in range(len(series_1)-29)]
    ax[0, 1].plot(rolling_dtw, color="red")
    ax[0, 1].set_title("Rolling DTW Distance (Window=30)")
    
    # DTW Warping Path Density
    _, paths = dtw.warping_paths(series_1, series_2)
    path_x, path_y = zip(*dtw.best_path(paths))
    sns.kdeplot(x=path_x, y=path_y, cmap="Reds", fill=True, ax=ax[1, 0])
    ax[1, 0].set_title("DTW Warping Path Density")
    
    # Stock Price Change Correlation
    aligned_1 = [series_1[i] for i, j in dtw.best_path(paths)]
    aligned_2 = [series_2[j] for i, j in dtw.best_path(paths)]
    ax[1, 1].scatter(np.diff(aligned_1), np.diff(aligned_2), alpha=0.5, color="green")
    ax[1, 1].set_title("Stock Price Change Correlation (Aligned by DTW)")
    
    plt.tight_layout()
    plt.show()

# Execute the analysis
stock_1, stock_2, period = get_user_input()
series_1, series_2 = fetch_stock_data(stock_1, period), fetch_stock_data(stock_2, period)
if series_1 is not None and series_2 is not None:
    min_length = min(len(series_1), len(series_2))
    series_1, series_2 = series_1[:min_length], series_2[:min_length]
    dtw_dist = compute_dtw(series_1, series_2, "DTW")
    mdtw_dist = compute_dtw(series_1, series_2, "MDTW")
    cdtw_dist = compute_dtw(series_1, series_2, "CDTW")
    normalized_dtw = compute_normalized_dtw(series_1, series_2)
    
    print(f"\nComparing {stock_1} and {stock_2} over {period}:")
    print(f"DTW Distance: {dtw_dist:.2f}")
    print(f"MDTW Distance (Downsampled): {mdtw_dist:.2f}")
    print(f"CDTW Distance (Constrained): {cdtw_dist:.2f}")
    print(f"Normalized DTW Distance: {normalized_dtw:.4f}")
    
    plot_stock_data(series_1, series_2, stock_1, stock_2)
    plot_alternative_dtw_visualizations(series_1, series_2)
