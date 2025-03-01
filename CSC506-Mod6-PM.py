import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Generate and print two time series data
def generate_time_series():
    np.random.seed(42)
    series1 = np.random.randint(1, 9, size=np.random.randint(10, 23))
    series2 = np.random.randint(1, 9, size=np.random.randint(10, 23))
    print("Time Series 1:", series1)
    print("Time Series 2:", series2)
    return series1, series2

time_series1, time_series2 = generate_time_series()

def dtw_distance(series_a, series_b):
    n, m = len(series_a), len(series_b)
    dtw_matrix = np.zeros((n+1, m+1)) + np.inf
    dtw_matrix[0, 0] = 0
    
    for i in range(1, n+1):
        for j in range(1, m+1):
            cost = abs(series_a[i-1] - series_b[j-1])
            dtw_matrix[i, j] = cost + min(dtw_matrix[i-1, j],    # Insertion
                                         dtw_matrix[i, j-1],    # Deletion
                                         dtw_matrix[i-1, j-1])  # Match
    
    # Reconstruct warping path
    i, j = n, m
    path = []
    while i > 0 and j > 0:
        path.append((i-1, j-1))
        i, j = min((i-1, j), (i, j-1), (i-1, j-1), key=lambda x: dtw_matrix[x])
    path.reverse()
    
    return dtw_matrix[1:, 1:], dtw_matrix[n, m], path

def plot_dtw(series_a, series_b, dtw_matrix, path):
    fig, ax = plt.subplots(1, 3, figsize=(18, 5))
    
    # Plot the time series
    ax[0].plot(series_a, label='Series A', marker='o')
    ax[0].plot(series_b, label='Series B', marker='s')
    ax[0].set_title("Time Series Comparison")
    ax[0].legend()
    
    # Plot the DTW cost matrix
    sns.heatmap(dtw_matrix, cmap='coolwarm', ax=ax[1])
    ax[1].set_title("DTW Cost Matrix")
    ax[1].invert_yaxis()
    
    # Plot warping path
    path_x, path_y = zip(*path)
    ax[2].plot(path_x, path_y, marker='o', linestyle='-')
    ax[2].set_title("Warping Path")
    ax[2].set_xlabel("Series A Index")
    ax[2].set_ylabel("Series B Index")
    
    plt.show()

def plot_aligned_series(series_a, series_b, path):
    aligned_a = [series_a[i] for i, j in path]
    aligned_b = [series_b[j] for i, j in path]
    
    plt.figure(figsize=(10, 5))
    plt.plot(aligned_a, label='Warped Series A', marker='o')
    plt.plot(aligned_b, label='Warped Series B', marker='s')
    plt.title("Aligned Time Series After DTW")
    plt.legend()
    plt.show()

# Compare and visualize DTW
dtw_matrix, distance, path = dtw_distance(time_series1, time_series2)
print(f"DTW Distance: {distance}")
plot_dtw(time_series1, time_series2, dtw_matrix, path)
plot_aligned_series(time_series1, time_series2, path)
