import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

print("Starting the Tire Strategy Analysis...")

# Define the data directory
data_dir = "data"

# Load the stints data
print("Loading stints data...")
stints_df = pd.read_csv(f"{data_dir}/stints_data.csv")
stints_df.columns = stints_df.columns.str.strip()  # Clean column names
print("Stints data loaded successfully.")

# Load the laps data
print("Loading laps data...")
laps_df = pd.read_csv(f"{data_dir}/lap_data.csv")
laps_df.columns = laps_df.columns.str.strip()  # Clean column names
print("Laps data loaded successfully.")

# Load the drivers data
print("Loading drivers data...")
drivers_df = pd.read_csv(f"{data_dir}/driver_data.csv")
drivers_df.columns = drivers_df.columns.str.strip()  # Clean column names
print("Drivers data loaded successfully.")

# Clean the driver_number column to ensure it's numeric
stints_df['driver_number'] = pd.to_numeric(stints_df['driver_number'], errors='coerce').astype('Int64')
laps_df['driver_number'] = pd.to_numeric(laps_df['driver_number'], errors='coerce').astype('Int64')
drivers_df['driver_number'] = pd.to_numeric(drivers_df['driver_number'], errors='coerce').astype('Int64')

# Merge stints data with drivers data to get driver names
stints_df = stints_df.merge(drivers_df[['driver_number', 'full_name']], on='driver_number')

# Plotting tire compounds used by each driver
print("Plotting tire compounds used by each driver...")
plt.figure(figsize=(14, 7))
sns.countplot(data=stints_df, x='full_name', hue='compound')
plt.title('Tire Compounds Used by Each Driver')
plt.xlabel('Driver')
plt.ylabel('Number of Stints')
plt.xticks(rotation=90)
plt.legend(title='Tire Compound')
plt.show()

# Merge stints data with laps data to analyze performance drop-off
print("Merging stints data with laps data...")
laps_df['lap_number'] = laps_df['lap_number'].astype(int)
stints_df['lap_start'] = stints_df['lap_start'].astype(int)
stints_df['lap_end'] = stints_df['lap_end'].astype(int)

# Initialize a list to store detailed lap data with tire compounds
detailed_lap_data = []

# Loop through each stint and associate laps with the compound used
for _, stint in stints_df.iterrows():
    driver_laps = laps_df[(laps_df['driver_number'] == stint['driver_number']) &
                          (laps_df['lap_number'] >= stint['lap_start']) &
                          (laps_df['lap_number'] <= stint['lap_end'])]
    driver_laps['compound'] = stint['compound']
    driver_laps['full_name'] = stint['full_name']
    detailed_lap_data.append(driver_laps)

# Concatenate all the detailed lap data
detailed_laps_df = pd.concat(detailed_lap_data)

# Plotting performance drop-off as tires age with Facet Grid
print("Plotting performance drop-off as tires age with Facet Grid...")
g = sns.FacetGrid(detailed_laps_df, col="compound", col_wrap=2, height=5, aspect=1.5)
g.map(sns.lineplot, "lap_number", "lap_duration", "full_name", alpha=0.6)
g.add_legend()
g.set_titles("{col_name} Compound")
g.set_axis_labels("Lap Number", "Lap Duration (seconds)")
plt.show()

print("Tire Strategy Analysis completed successfully.")
