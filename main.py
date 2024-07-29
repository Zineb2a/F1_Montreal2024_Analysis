import pandas as pd

print("Starting the data processing script...")


print("Loading datasets...")
drivers_df = pd.read_csv("driver_data.csv")
intervals_df = pd.read_csv("interval_data.csv")
laps_df = pd.read_csv("lap_data.csv")
pit_df = pd.read_csv("pit_stop_data.csv")
race_control_df = pd.read_csv("race_control_data.csv")
stints_df = pd.read_csv("stints_data.csv")
weather_df = pd.read_csv("weather_data.csv")
print("Datasets loaded successfully.")


dataset_names = ["Drivers", "Intervals", "Laps", "Pit", "Race Control", "Stints", "Weather"]

# Remove duplicates
print("Removing duplicates...")
datasets = [drivers_df, intervals_df, laps_df, pit_df, race_control_df, stints_df, weather_df]
for df, name in zip(datasets, dataset_names):
    initial_count = len(df)
    df.drop_duplicates(inplace=True)
    print(f"Removed {initial_count - len(df)} duplicates from {name}.")
print("Duplicates removed.")

# Handle missing values (example: fill with mean for numerical columns)
print("Handling missing values...")
for df, name in zip(datasets, dataset_names):
    numeric_cols = df.select_dtypes(include=[float, int]).columns
    for col in numeric_cols:
        missing_count = df[col].isna().sum()
        df[col] = df[col].fillna(df[col].mean())
        print(f"Filled {missing_count} missing values in {col} of {name}.")
print("Missing values handled.")

# Convert date columns to datetime
print("Converting date columns to datetime...")
for df, name in zip(datasets, dataset_names):
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
        print(f"Converted date column in {name}.")
print("Date columns converted.")

# Convert relevant columns to integers
print("Converting relevant columns to integers...")
int_cols = ['driver_number', 'session_key', 'meeting_key', 'lap_number']
for df, name in zip(datasets, dataset_names):
    for col in int_cols:
        if col in df.columns:
            df[col] = df[col].apply(lambda x: int(x) if pd.notnull(x) and x.is_integer() else pd.NA)
            df[col] = df[col].astype(pd.Int64Dtype())
            print(f"Converted {col} to integers in {name}.")
print("Relevant columns converted to integers.")

# Print info to check data types and missing values
print("Checking data types and missing values...")
for df, name in zip(datasets, dataset_names):
    print(f"{name} DataFrame Info:\n", df.info(), "\n")
print("Data types and missing values checked.")

# Merge datasets using common keys
print("Merging datasets...")
merged_df = laps_df.merge(drivers_df, on=['driver_number', 'session_key', 'meeting_key'], how='left')
print("Merged laps and drivers data.")
merged_df = merged_df.merge(intervals_df, on=['driver_number', 'session_key', 'meeting_key'], how='left')
print("Merged intervals data.")
merged_df = merged_df.merge(pit_df, on=['driver_number', 'session_key', 'meeting_key', 'lap_number'], how='left')
print("Merged pit stop data.")
merged_df = merged_df.merge(race_control_df, on=['driver_number', 'session_key', 'meeting_key', 'lap_number'], how='left')
print("Merged race control data.")
merged_df = merged_df.merge(stints_df, on=['driver_number', 'session_key', 'meeting_key'], how='left')
print("Merged stints data.")
merged_df = merged_df.merge(weather_df, on=['session_key', 'meeting_key', 'date'], how='left')
print("Merged weather data.")

# Check the merged DataFrame
print("Checking merged DataFrame...")
print("Merged DataFrame Info:\n", merged_df.info(), "\n")
print("Merged DataFrame Head:\n", merged_df.head(), "\n")
print("Merged DataFrame checked.")

# Save the cleaned and merged DataFrame to a CSV file
print("Saving merged DataFrame to CSV...")
merged_df.to_csv("merged_data.csv", index=False)
print("Merged DataFrame saved to merged_data.csv.")


print("Script completed successfully.")
