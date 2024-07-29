import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

print("Starting the Pit Stop Strategy Analysis...")

# Define the data directory
data_dir = "data"

# Load the pit stop data
print("Loading pit stop data...")
pit_df = pd.read_csv(f"{data_dir}/pit_stop_data.csv")
pit_df.columns = pit_df.columns.str.strip()  # Clean column names
print("Pit stop data loaded successfully.")

# Load the drivers data
print("Loading drivers data...")
drivers_df = pd.read_csv(f"{data_dir}/driver_data.csv")
drivers_df.columns = drivers_df.columns.str.strip()  # Clean column names
print("Drivers data loaded successfully.")

# Load the ranking data
print("Loading ranking data...")
ranking_df = pd.read_csv(f"{data_dir}/ranking_data.csv")
ranking_df.columns = ranking_df.columns.str.strip()  # Clean column names
print("Ranking data loaded successfully.")

# Process the ranking data to get the final positions
print("Processing ranking data to get final positions...")
ranking_df['date'] = pd.to_datetime(ranking_df['date'])
final_positions = ranking_df.sort_values(by=['driver_number', 'date']).drop_duplicates(subset=['driver_number'], keep='last')
final_positions = final_positions.rename(columns={"position": "final_position"})  # Rename for consistency

# Calculate the number of pit stops per driver
print("Calculating the number of pit stops per driver...")
pit_stops_per_driver = pit_df.groupby('driver_number').size().reset_index(name='num_pit_stops')

# Calculate the average pit stop duration per driver
print("Calculating the average pit stop duration per driver...")
avg_pit_duration_per_driver = pit_df.groupby('driver_number')['pit_duration'].mean().reset_index(name='avg_pit_duration')

# Merge pit stop data with final positions and driver names
pit_stop_analysis = final_positions.merge(pit_stops_per_driver, on='driver_number').merge(avg_pit_duration_per_driver, on='driver_number')
pit_stop_analysis = pit_stop_analysis.merge(drivers_df[['driver_number', 'full_name', 'team_name']], on='driver_number')

# Plotting number of pit stops per driver
print("Plotting number of pit stops per driver...")
plt.figure(figsize=(12, 6))
sns.barplot(data=pit_stop_analysis, x='full_name', y='num_pit_stops', palette='viridis')
plt.title('Number of Pit Stops per Driver')
plt.xlabel('Driver')
plt.ylabel('Number of Pit Stops')
plt.xticks(rotation=90)
plt.show()

# Plotting average pit stop duration per driver
print("Plotting average pit stop duration per driver...")
plt.figure(figsize=(12, 6))
sns.barplot(data=pit_stop_analysis, x='full_name', y='avg_pit_duration', palette='viridis')
plt.title('Average Pit Stop Duration per Driver')
plt.xlabel('Driver')
plt.ylabel('Average Pit Stop Duration (seconds)')
plt.xticks(rotation=90)
plt.show()

# Analyze the impact of pit stops on lap times and final positions
print("Analyzing the impact of pit stops on lap times and final positions...")
laps_df = pd.read_csv(f"{data_dir}/lap_data.csv")
laps_df.columns = laps_df.columns.str.strip()  # Clean column names
laps_df['lap_duration'] = pd.to_numeric(laps_df['lap_duration'], errors='coerce')

# Merge laps data with pit stop data
merged_laps_pits = laps_df.merge(pit_df[['driver_number', 'lap_number', 'pit_duration']], on=['driver_number', 'lap_number'], how='left')
merged_laps_pits['pit_stop'] = ~merged_laps_pits['pit_duration'].isna()

# Plot lap times with and without pit stops
print("Plotting lap times with and without pit stops...")
plt.figure(figsize=(14, 7))
sns.lineplot(data=merged_laps_pits, x='lap_number', y='lap_duration', hue='pit_stop')
plt.title('Lap Times with and without Pit Stops')
plt.xlabel('Lap Number')
plt.ylabel('Lap Duration (seconds)')
plt.legend(title='Pit Stop', labels=['No Pit Stop', 'Pit Stop'])
plt.show()

# Analyzing the impact of pit stops on final positions
print("Analyzing the impact of pit stops on final positions...")
plt.figure(figsize=(10, 6))
sns.scatterplot(data=pit_stop_analysis, x='num_pit_stops', y='final_position', hue='team_name', alpha=0.6)

for i, row in pit_stop_analysis.iterrows():
    plt.text(row['num_pit_stops'], row['final_position'], row['full_name'], fontsize=9)

plt.title('Impact of Number of Pit Stops on Final Positions')
plt.xlabel('Number of Pit Stops')
plt.ylabel('Final Position')
plt.gca().invert_yaxis()  # Invert y-axis to have 1 at the top
plt.legend(title='Team Name', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.show()

plt.figure(figsize=(10, 6))
sns.scatterplot(data=pit_stop_analysis, x='avg_pit_duration', y='final_position', hue='team_name', alpha=0.6)

for i, row in pit_stop_analysis.iterrows():
    plt.text(row['avg_pit_duration'], row['final_position'], row['full_name'], fontsize=9)

plt.title('Impact of Average Pit Stop Duration on Final Positions')
plt.xlabel('Average Pit Stop Duration (seconds)')
plt.ylabel('Final Position')
plt.gca().invert_yaxis()  # Invert y-axis to have 1 at the top
plt.legend(title='Team Name', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.show()

print("Pit Stop Strategy Analysis completed successfully.")
