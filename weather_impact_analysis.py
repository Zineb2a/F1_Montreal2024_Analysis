import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

print("Starting the Weather Impact Analysis...")

# Define the data directory
data_dir = "data"

# Load the weather data
print("Loading weather data...")
weather_df = pd.read_csv(f"{data_dir}/weather_data.csv")
weather_df.columns = weather_df.columns.str.strip()  # Clean column names
weather_df['date'] = pd.to_datetime(weather_df['date'], errors='coerce')
print("Weather data loaded successfully.")

# Load the laps data
print("Loading laps data...")
laps_df = pd.read_csv(f"{data_dir}/lap_data.csv")
laps_df.columns = laps_df.columns.str.strip()  # Clean column names
laps_df['date_start'] = pd.to_datetime(laps_df['date_start'], errors='coerce')
laps_df = laps_df.dropna(subset=['date_start'])  # Drop rows with null date_start
print("Laps data loaded successfully.")

# Load the race control data
print("Loading race control data...")
race_control_df = pd.read_csv(f"{data_dir}/race_control_data.csv")
race_control_df.columns = race_control_df.columns.str.strip()  # Clean column names
race_control_df['date'] = pd.to_datetime(race_control_df['date'], errors='coerce')
print("Race control data loaded successfully.")

# Merge laps data with weather data based on the closest timestamp
print("Merging laps data with weather data...")
merged_laps_weather = pd.merge_asof(laps_df.sort_values('date_start'), 
                                    weather_df.sort_values('date'), 
                                    left_on='date_start', right_on='date')

# Plotting the combined weather conditions against lap times
print("Plotting combined weather conditions against lap times...")
plt.figure(figsize=(14, 7))

# Plot Track Temperature
sns.lineplot(data=merged_laps_weather, x='date_start', y='track_temperature', label='Track Temperature (°C)', color='red')

# Plot Air Temperature on secondary y-axis
ax2 = plt.twinx()
sns.lineplot(data=merged_laps_weather, x='date_start', y='air_temperature', label='Air Temperature (°C)', color='blue', ax=ax2)
ax2.set_ylabel('Air Temperature (°C)')

# Plot Humidity on the same secondary y-axis
sns.lineplot(data=merged_laps_weather, x='date_start', y='humidity', label='Humidity (%)', color='green', ax=ax2)

# Plot Wind Speed on another secondary y-axis
ax3 = plt.twinx()
ax3.spines['right'].set_position(('outward', 60))
sns.lineplot(data=merged_laps_weather, x='date_start', y='wind_speed', label='Wind Speed (m/s)', color='purple', ax=ax3)
ax3.set_ylabel('Wind Speed (m/s)')

plt.title('Combined Weather Conditions Against Lap Times')
plt.xlabel('Time')
plt.legend(loc='upper left')
plt.show()

# Analyze incidents recorded in race control data to see if they coincide with weather changes
print("Analyzing incidents in race control data and their correlation with weather changes...")
merged_incidents_weather = pd.merge_asof(race_control_df.sort_values('date'), 
                                         weather_df.sort_values('date'), 
                                         on='date')

plt.figure(figsize=(14, 7))
sns.scatterplot(data=merged_incidents_weather, x='date', y='track_temperature', hue='category', style='category', palette='tab10', s=100)
plt.title('Incidents vs Track Temperature')
plt.xlabel('Time')
plt.ylabel('Track Temperature (°C)')
plt.legend(title='Incident Type', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.show()

plt.figure(figsize=(14, 7))
sns.scatterplot(data=merged_incidents_weather, x='date', y='air_temperature', hue='category', style='category', palette='tab10', s=100)
plt.title('Incidents vs Air Temperature')
plt.xlabel('Time')
plt.ylabel('Air Temperature (°C)')
plt.legend(title='Incident Type', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.show()

plt.figure(figsize=(14, 7))
sns.scatterplot(data=merged_incidents_weather, x='date', y='humidity', hue='category', style='category', palette='tab10', s=100)
plt.title('Incidents vs Humidity')
plt.xlabel('Time')
plt.ylabel('Humidity (%)')
plt.legend(title='Incident Type', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.show()

print("Weather Impact Analysis completed successfully.")

