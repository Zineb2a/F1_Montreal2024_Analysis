import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

print("Starting the Qualifying vs. Race Performance Analysis...")

# Define the data directory
data_dir = "data"

# Load the ranking data
print("Loading ranking data...")
ranking_df = pd.read_csv(f"{data_dir}/ranking_data.csv")
ranking_df.columns = ranking_df.columns.str.strip()  # Clean column names
print("Ranking data loaded successfully.")

# Load the drivers data
print("Loading drivers data...")
drivers_df = pd.read_csv(f"{data_dir}/driver_data.csv")
drivers_df.columns = drivers_df.columns.str.strip()  # Clean column names
print("Drivers data loaded successfully.")

# Process the ranking data to get the final positions
print("Processing ranking data to get final positions...")
ranking_df['date'] = pd.to_datetime(ranking_df['date'])
final_positions = ranking_df.sort_values(by=['driver_number', 'date']).drop_duplicates(subset=['driver_number'], keep='last')
final_positions = final_positions.rename(columns={"position": "final_position"})  # Rename for consistency

# Process the ranking data to get starting (qualifying) positions
print("Processing ranking data to get starting positions...")
starting_positions = ranking_df.sort_values(by=['driver_number', 'date']).drop_duplicates(subset=['driver_number'], keep='first')
starting_positions = starting_positions.rename(columns={"position": "starting_position"})  # Rename for consistency

# Merge ranking data with driver data to get final positions with driver names
final_positions = final_positions.merge(drivers_df[['driver_number', 'full_name']], on='driver_number')
starting_positions = starting_positions.merge(drivers_df[['driver_number', 'full_name']], on='driver_number')

# Merge qualifying data with final positions
performance_comparison = final_positions.merge(starting_positions[['driver_number', 'starting_position']], on='driver_number')

# Plotting starting vs. ending positions
print("Plotting starting vs. ending positions...")
plt.figure(figsize=(10, 6))
sns.scatterplot(data=performance_comparison, x='starting_position', y='final_position', hue='full_name', alpha=0.6)

for i, row in performance_comparison.iterrows():
    plt.text(row['starting_position'], row['final_position'], row['full_name'], fontsize=9)

plt.title('Starting vs. Ending Positions')
plt.xlabel('Starting Position')
plt.ylabel('Final Position')
plt.gca().invert_yaxis()  # Invert y-axis to have 1 at the top
plt.show()

# Step 5: Analyze Position Changes

print("Analyzing position changes...")

# Calculate position changes
performance_comparison['position_change'] = performance_comparison['starting_position'] - performance_comparison['final_position']

# Plotting position changes
print("Plotting position changes...")
plt.figure(figsize=(12, 6))
sns.barplot(data=performance_comparison, x='full_name', y='position_change', palette='viridis')
plt.title('Position Changes from Qualifying to Race')
plt.xlabel('Driver')
plt.ylabel('Position Change (Positive = Improvement, Negative = Decline)')
plt.xticks(rotation=90)
plt.show()

print("Qualifying vs. Race Performance analysis completed successfully.")
