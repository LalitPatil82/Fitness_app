import pandas as pd
import sqlite3

# Load CSV files into Pandas DataFrames
df_exercise = pd.read_csv("exercise.csv")
df_calories = pd.read_csv("calories.csv")

# Merge the datasets on 'User_ID'
df_merged = pd.merge(df_exercise, df_calories, on="User_ID")

# Save merged data to a new CSV file (optional)
df_merged.to_csv("merged_fitness_data.csv", index=False)

# Display first few rows
print(df_merged.head())

# Create SQLite database connection
conn = sqlite3.connect("fitness_tracker.db")
cursor = conn.cursor()

# Save DataFrames into SQLite tables
df_exercise.to_sql("exercise", conn, if_exists="replace", index=False)
df_calories.to_sql("calories", conn, if_exists="replace", index=False)
df_merged.to_sql("merged_data", conn, if_exists="replace", index=False)

# Verify if tables exist
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
print("Tables in the database:", cursor.fetchall())


query = "SELECT * FROM exercise JOIN calories ON exercise.User_ID = calories.User_ID;"
df_sql_merged = pd.read_sql(query, conn)
print(df_sql_merged.head())


query = """
SELECT * FROM merged_data
WHERE Height BETWEEN 140 AND 205 
AND Body_Temp <= 41.2 
AND Calories >= 5;
"""
df_cleaned = pd.read_sql(query, conn)
print(df_cleaned.head())


query = """
SELECT 
    CASE 
        WHEN Age BETWEEN 20 AND 29 THEN '20s'
        WHEN Age BETWEEN 30 AND 39 THEN '30s'
        WHEN Age BETWEEN 40 AND 49 THEN '40s'
        WHEN Age BETWEEN 50 AND 59 THEN '50s'
        WHEN Age BETWEEN 60 AND 69 THEN '60s'
        ELSE '70s'
    END AS Age_Group,
    AVG(Calories) AS Avg_Calories
FROM merged_data
GROUP BY Age_Group;
"""
df_calories_by_age = pd.read_sql(query, conn)
print(df_calories_by_age)

df_cleaned.to_csv("cleaned_fitness_data.csv", index=False)
print("Cleaned data saved successfully!")
