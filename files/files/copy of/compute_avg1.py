import pandas as pd
import numpy as np

# Load the CSV file
camera_log = pd.read_csv('path/to/your/camera_log.csv')

# Convert data to numeric, handling non-numeric data
camera_log = camera_log.apply(pd.to_numeric, errors='coerce')

# Function to normalize yaw to range [-180, 180)
def normalize_yaw(yaw):
    yaw = yaw % 360
    if yaw > 180:
        yaw -= 360
    return yaw

# Apply normalization
for camera in ['Camera 1 Yaw', 'Camera 2 Yaw', 'Camera 3 Yaw', 'Camera 4 Yaw']:
    camera_log[camera] = camera_log[camera].apply(normalize_yaw)

# Adjust yaw values so opposite cameras sum to zero
camera_log['Camera 3 Yaw'] = -camera_log['Camera 1 Yaw']
camera_log['Camera 4 Yaw'] = -camera_log['Camera 2 Yaw']

# Adjust cross-camera relationships for pitch and yaw
camera_log['Camera 2 Yaw'] = camera_log['Camera 1 Pitch']
camera_log['Camera 3 Pitch'] = -camera_log['Camera 2 Yaw']
camera_log['Camera 4 Yaw'] = camera_log['Camera 3 Pitch']
camera_log['Camera 1 Pitch'] = -camera_log['Camera 4 Yaw']

# Calculate the average pitch and yaw for each timestamp
camera_log['Average Pitch'] = camera_log[['Camera 1 Pitch', 'Camera 2 Pitch', 'Camera 3 Pitch', 'Camera 4 Pitch']].mean(axis=1)
camera_log['Average Yaw'] = camera_log[['Camera 1 Yaw', 'Camera 2 Yaw', 'Camera 3 Yaw', 'Camera 4 Yaw']].mean(axis=1)

# Save the processed data to a new CSV file
camera_log.to_csv('processed_camera_log.csv', index=False)

# Print the first few rows of the dataframe to check the result
print(camera_log.head())

