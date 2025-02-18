# CSC505 Module 4 Portfolio Milestone
# Algorithm Implementation and Testing.

# Importing necessary libraries
import yfinance as yf
import numpy as np
from dtaidistance import dtw
import pandas as pd
import matplotlib.pyplot as plt

# Fetching historical stock price data
ticker_1 = yf.Ticker("F")
ticker_2 = yf.Ticker("GM")

# Get data for the last year
data_1 = ticker_1.history(period="1y")
data_2 = ticker_2.history(period="1y")

# Use the closing price for comparison
series_1 = data_1['Close'].values
series_2 = data_2['Close'].values

# Check for missing values and handle them
series_1 = pd.Series(series_1).ffill().values
series_2 = pd.Series(series_2).ffill().values

# Ensure both series are of equal length
min_length = min(len(series_1), len(series_2))
series_1 = series_1[:min_length]
series_2 = series_2[:min_length]

# Calculate DTW distance
distance = dtw.distance(series_1, series_2)
print(f"DTW distance: {distance}")

# MDTW Implementation
# Downsample the series (taking every second element)
downsampled_1 = series_1[::2]
downsampled_2 = series_2[::2]

# Calculate DTW distance on downsampled series
mdtw_distance = dtw.distance(downsampled_1, downsampled_2)
print(f"MDTW distance: {mdtw_distance:.2f}")

# CDTW Implementation
# Define window size for CDTW
window_size = 10

# Calculate CDTW distance with the specified window size
cdtw_distance = dtw.distance(series_1, series_2, window=window_size)
print(f"CDTW distance: {cdtw_distance:.2f}")

# Visualization
plt.figure(figsize=(10, 6))
plt.plot(data_1.index[:min_length], series_1, label="F", color="blue")
plt.plot(data_2.index[:min_length], series_2, label="GM", color="green")
plt.title("Stock Price Comparison: F vs GM")
plt.xlabel("Date")
plt.ylabel("Closing Price (USD)")
plt.legend()
plt.show()