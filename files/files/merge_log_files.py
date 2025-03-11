import pandas as pd

# Load the two CSV files
file_a = 'file_a.csv'  # Replace with the actual path to your file A
file_b = 'file_b.csv'  # Replace with the actual path to your file B

# Read the CSV files into DataFrames
df_a = pd.read_csv(file_a)
df_b = pd.read_csv(file_b)

# Convert timestamp columns to datetime format for proper comparison and merging
df_a['Timestamp'] = pd.to_datetime(df_a['Timestamp'])
df_b['Timestamp'] = pd.to_datetime(df_b['Timestamp'])

# Merge the two DataFrames on the 'Timestamp' column
merged_df = pd.merge(df_a, df_b, on='Timestamp', how='outer', suffixes=('_algorithm', '_imu'))

# Compare data and integrate as necessary
# For example, you could create new columns to show the difference between the IMU and algorithm values
merged_df['Pitch Difference'] = merged_df['Average Pitch_algorithm'] - merged_df['Pitch_imu']
merged_df['Yaw Difference'] = merged_df['Average Yaw_algorithm'] - merged_df['Yaw_imu']

# Save the resulting DataFrame to a new CSV file
merged_df.to_csv('integrated_camera_imu_data.csv', index=False)

# Print the first few rows of the integrated table to check the result
print(merged_df.head())

