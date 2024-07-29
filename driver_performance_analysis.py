import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import requests

print("Starting the Driver Performance Analysis using non-merged data...")


data_dir = "data"

# Fetch the ranking data
def fetch_ranking_data(session_key):
    url = f"https://api.openf1.org/v1/position?session_key={session_key}&csv=true"
    response = requests.get(url)
    if response.status_code == 200:
        with open("{data_dir}/ranking_data.csv", "wb") as file:
            file.write(response.content)
        print("Ranking data fetched and saved successfully.")
    else:
        print(f"Failed to fetch data: {response.status_code}")


fetch_ranking_data(9531)

# Load the fetched ranking data
print("Loading ranking data...")
ranking_df = pd.read_csv("{data_dir}/ranking_data.csv")
ranking_df.columns = ranking_df.columns.str.strip()  # Clean column names
print("Ranking data loaded successfully.")

# Step 1: Distribution of Driver Nationalities

# Load drivers data
print("Loading drivers data...")
drivers_df = pd.read_csv("{data_dir}/driver_data.csv")
drivers_df.columns = drivers_df.columns.str.strip()  # Clean column names
print("Drivers data loaded successfully.")

# Inspect the cleaned columns
print("Cleaned Drivers DataFrame columns:", drivers_df.columns)

# Plotting the distribution of driver nationalities
print("Plotting the distribution of driver nationalities...")
plt.figure(figsize=(12, 6))
sns.countplot(data=drivers_df, x='country_code')
plt.title('Distribution of Driver Nationalities')
plt.xlabel('Country Code')
plt.ylabel('Number of Drivers')
plt.xticks(rotation=45)
plt.show()

# Step 2: Evolution of Drivers' Lap Times

# Load laps data
print("Loading laps data...")
laps_df = pd.read_csv("{data_dir}/lap_data.csv")
laps_df.columns = laps_df.columns.str.strip()  # Clean column names
print("Laps data loaded successfully.")

# Convert lap_duration to numeric
laps_df['lap_duration'] = pd.to_numeric(laps_df['lap_duration'], errors='coerce')

# Merge laps data with drivers data to get driver names
print("Merging laps data with driver names...")
laps_df = laps_df.merge(drivers_df[['driver_number', 'full_name']], on='driver_number', how='left')

# Plot lap times for each driver across the race with unique colors and jitter
print("Plotting lap times for each driver across the race...")
plt.figure(figsize=(14, 8))
unique_drivers = laps_df['full_name'].unique()
colors = plt.cm.get_cmap('tab20', len(unique_drivers)).colors

for driver, color in zip(unique_drivers, colors):
    driver_laps = laps_df[laps_df['full_name'] == driver]
    plt.plot(driver_laps['lap_number'], driver_laps['lap_duration'], label=driver, color=color, alpha=0.6, linestyle='', marker='o')

plt.title('Lap Times Evolution Over the Race')
plt.xlabel('Lap Number')
plt.ylabel('Lap Duration (seconds)')
plt.legend(loc='upper right', bbox_to_anchor=(1.1, 1.05))
plt.show()

# Step 3: Correlation Between Lap Times and Final Race Positions

# Process the ranking data to get the final positions
print("Processing ranking data to get final positions...")
ranking_df['date'] = pd.to_datetime(ranking_df['date'])
ranking_df = ranking_df.sort_values(by=['driver_number', 'date']).drop_duplicates(subset=['driver_number'], keep='last')
ranking_df = ranking_df.rename(columns={"position": "final_position"})  # Rename for consistency

# Merging ranking data with driver data to get final positions with driver names
final_positions = ranking_df.merge(drivers_df[['driver_number', 'full_name']], on='driver_number')

# Calculate average lap time for each driver
print("Calculating average lap times for each driver...")
avg_lap_times = laps_df.groupby('driver_number')['lap_duration'].mean().reset_index()
avg_lap_times.columns = ['driver_number', 'avg_lap_duration']

# Merging average lap times with final race positions
print("Merging average lap times with final race positions...")
driver_performance = avg_lap_times.merge(final_positions[['driver_number', 'final_position', 'full_name']], on='driver_number')

# Correlation plot with driver names
print("Plotting correlation between average lap times and final race positions...")
plt.figure(figsize=(10, 6))
sns.scatterplot(data=driver_performance, x='avg_lap_duration', y='final_position', alpha=0.6)

# Annotate each point with the driver's name
for i, row in driver_performance.iterrows():
    plt.text(row['avg_lap_duration'], row['final_position'], row['full_name'], fontsize=9)

plt.title('Correlation Between Average Lap Times and Final Race Positions')
plt.xlabel('Average Lap Duration (seconds)')
plt.ylabel('Final Race Position')
plt.gca().invert_yaxis()  # Invert y-axis to have 1 at the top
plt.show()

# Calculate correlation coefficient
correlation = driver_performance['avg_lap_duration'].corr(driver_performance['final_position'])
print(f"Correlation between average lap times and final race positions: {correlation}")

print("Driver Performance Analysis script completed successfully.")

