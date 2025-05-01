import numpy as np

# Generate a large dataset (e.g., 10 million random numbers)
large_dataset = np.random.rand(10_000_000)

# Basic statistics
mean = np.mean(large_dataset)
std_dev = np.std(large_dataset)
print(f"Mean: {mean}, Standard Deviation: {std_dev}")

# Perform a mathematical operation (e.g., normalize the dataset)
normalized_dataset = (large_dataset - mean) / std_dev

# Find elements greater than a threshold
threshold = 1.0
filtered_elements = normalized_dataset[normalized_dataset > threshold]
print(f"Number of elements greater than {threshold}: {len(filtered_elements)}")

# Reshape the dataset into a 2D array
reshaped_dataset = large_dataset.reshape(10_000, 1_000)
print(f"Reshaped dataset shape: {reshaped_dataset.shape}")

# Perform matrix multiplication on large arrays
matrix_a = np.random.rand(1000, 1000)
matrix_b = np.random.rand(1000, 1000)
result = np.dot(matrix_a, matrix_b)
print(f"Matrix multiplication result shape: {result.shape}")