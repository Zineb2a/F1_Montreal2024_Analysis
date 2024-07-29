# F1 Race Analysis Project

This project aims to analyze the performance and various aspects of the F1 Montreal Grand Prix 2024 using data analysis techniques. The analysis includes driver performance, pit stop strategies, tire strategies, weather impact, and incidents during the race. The data is fetched from the OpenF1 API and processed using Python.

## Technologies Used

- **Python**: The primary programming language used for data analysis.
- **Pandas**: Used for data manipulation and analysis.
- **NumPy**: Used for numerical operations.
- **Matplotlib**: Used for data visualization.
- **Seaborn**: Used for statistical data visualization.
- **scikit-learn**: Used for machine learning algorithms (if required).
- **Requests**: Used to fetch data from the OpenF1 API.


## Project Overview

### 1. Driver Performance Analysis

- **Questions Addressed**:
  - What is the distribution of driver nationalities in this dataset?
  - How did drivers' lap times evolve over the course of the race?
  - What is the correlation between lap times and final race positions?
  
### 2. Qualifying vs. Race Performance Analysis

- **Questions Addressed**:
  - How did qualifying positions correlate with final race positions?
  - Were there significant position gains or losses from the start to the end of the race?


### 3. Pit Stop Strategy Analysis

- **Questions Addressed**:
  - How many pit stops did each driver make, and how did the timing of these stops affect their performance?
  - What was the average pit stop duration, and how did it compare across different teams?


### 4. Tire Strategy Analysis

- **Questions Addressed**:
  - What tire strategies were employed, and how did they impact performance?
  - How did tire wear affect lap times towards the end of the race?

### 5. Weather Impact Analysis

- **Questions Addressed**:
  - How did weather conditions affect lap times and overall performance?
  - Were there any significant incidents due to weather conditions?

### 6. Incident Analysis

- **Questions Addressed**:
  - Analyze the distribution of incidents across different laps.
  - Breakdown of different types of incidents.
  - Correlate incidents with specific race events.

## Setting Up the Environment

### Step 1: Create a new environment

```bash
python3 -m venv f1_analysis_env
```

### Step 2: Activate the new environment

For macOS and Linux:
```bash
source f1_analysis_env/bin/activate
```

For Windows:
```bash
.\f1_analysis_env\Scripts\activate
```

### Step 3: Install the necessary packages

```bash
pip install pandas numpy matplotlib scikit-learn seaborn requests
```

## Running the Scripts

### Driver Performance Analysis

```bash
python driver_performance_analysis.py
```

### Qualifying vs. Race Performance Analysis

```bash
python qualifying_vs_race_performance_analysis.py
```

### Pit Stop Strategy Analysis

```bash
python pit_stop_strategy_analysis.py
```

### Tire Strategy Analysis

```bash
python tire_strategy_analysis.py
```

### Weather Impact Analysis

```bash
python weather_impact_analysis.py
```

### Incident Analysis

```bash
python combined_incident_analysis.py
```

For any questions or further information, please feel free to contact me.
