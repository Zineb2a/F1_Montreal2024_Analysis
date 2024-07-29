import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

print("Starting the Combined Incident Analysis using race control data...")

# Define the data directory
data_dir = "data"

# Load the race control data
print("Loading race control data...")
race_control_df = pd.read_csv(f"{data_dir}/race_control_data.csv")
race_control_df.columns = race_control_df.columns.str.strip()  # Clean column names
race_control_df['date'] = pd.to_datetime(race_control_df['date'], errors='coerce')
print("Race control data loaded successfully.")

# Incident Analysis by Lap Number and Incident Types combined
print("Analyzing incidents by lap number and types...")
plt.figure(figsize=(14, 7))
ax1 = sns.histplot(data=race_control_df, x='lap_number', hue='category', multiple='stack', palette='viridis', bins=20)
ax1.set_title('Incidents by Lap Number and Types')
ax1.set_xlabel('Lap Number')
ax1.set_ylabel('Number of Incidents')

# Ensure the legend is clearly displayed
handles, labels = ax1.get_legend_handles_labels()
ax1.legend(handles=handles, labels=labels, title='Incident Type', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()

# Incident Timing Analysis combined with Incident Types
print("Analyzing incident timing and types...")
plt.figure(figsize=(14, 7))
ax2 = sns.histplot(data=race_control_df, x='date', hue='category', multiple='stack', palette='viridis', bins=50, kde=True)
ax2.set_title('Incident Timing and Types')
ax2.set_xlabel('Time')
ax2.set_ylabel('Number of Incidents')

# Ensure the legend is clearly displayed
handles, labels = ax2.get_legend_handles_labels()
ax2.legend(handles=handles, labels=labels, title='Incident Type', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()

print("Combined Incident Analysis completed successfully.")
