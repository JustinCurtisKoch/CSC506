import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

#series_a = np.array([1, 2, 3, 3, 2, 1, 1, 2])
#series_b = np.array([1, 3, 3, 1, 1, 1, 3, 3])

# Generate and print time series data
def generate_time_series():
    np.random.seed(42)
    series_a = np.random.randint(1, 10, size=np.random.randint(11, 24))
    series_b = np.random.randint(1, 10, size=np.random.randint(11, 24))
    print("Time Series A:", series_a)
    print("Time Series B:", series_b)
    return series_a, series_b

series_a, series_b = generate_time_series()

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

def visualize_dtw(series_a, series_b, dtw_matrix, path):
    fig, ax = plt.subplots(2, 3, figsize=(18, 10))
    
    # Plot the time series
    ax[0, 0].plot(series_a, label='Series A', marker='o')
    ax[0, 0].plot(series_b, label='Series B', marker='s')
    ax[0, 0].set_title("Time Series Comparison")
    ax[0, 0].legend()
    
    # Plot the DTW cost matrix
    sns.heatmap(dtw_matrix, cmap='coolwarm', ax=ax[0, 1])
    ax[0, 1].set_title("DTW Cost Matrix")
    ax[0, 1].invert_yaxis()
    
    # Plot warping path
    path_x, path_y = zip(*path)
    ax[1, 0].plot(path_x, path_y, marker='o', linestyle='-')
    ax[1, 0].set_title("Warping Path")
    ax[1, 0].set_xlabel("Series A Index")
    ax[1, 0].set_ylabel("Series B Index")
    
    # Plot aligned series
    aligned_a = [series_a[i] for i, j in path]
    aligned_b = [series_b[j] for i, j in path]
    ax[1, 1].plot(aligned_a, label='Warped Series A', marker='o')
    ax[1, 1].plot(aligned_b, label='Warped Series B', marker='s')
    ax[1, 1].set_title("Aligned Time Series After DTW")
    ax[1, 1].legend()
    
    # Plot Euclidean and DTW alignment
    ax[0, 2].plot(series_a, label='Series A', marker='o', linestyle='-')
    ax[0, 2].plot(series_b, label='Series B', marker='s', linestyle='-')
    for i in range(min(len(series_a), len(series_b))):
        ax[0, 2].plot([i, i], [series_a[i], series_b[i]], 'k--')
    ax[0, 2].set_title("Euclidean Distance Alignment")
    ax[0, 2].legend()
    
    ax[1, 2].plot(series_a, label='Series A', marker='o', linestyle='-')
    ax[1, 2].plot(series_b, label='Series B', marker='s', linestyle='-')
    for i, j in path:
        ax[1, 2].plot([i, j], [series_a[i], series_b[j]], 'k--')
    ax[1, 2].set_title("DTW Alignment")
    ax[1, 2].legend()
    
    plt.tight_layout()
    plt.show()

# Compare and visualize DTW
dtw_matrix, distance, path = dtw_distance(series_a, series_b)
print(f"DTW Distance: {distance}")
visualize_dtw(series_a, series_b, dtw_matrix, path)
