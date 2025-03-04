from sklearn.linear_model import LinearRegression
import pandas as pd
import numpy as np

def predict_weight(user_data, age, height):
    # For demonstration, we'll create a simple model assuming weight loss based on calories burned
    # This is a very simplistic approach and not accurate for real-life use
    user_data['Calories Burned'] = user_data['Calories Burned'].astype(float)
    user_data['Cumulative Calories'] = user_data['Calories Burned'].cumsum()
    
    # Features and target
    X = user_data[['Cumulative Calories']]
    y = user_data['Calories Burned']  # Assuming initial weight is proportional to calories burned
    
    # Dummy initial weight
    initial_weight = 70
    
    # Fit model
    model = LinearRegression()
    model.fit(X, y)
    
    # Predict weight loss
    predicted_calories = user_data['Cumulative Calories'].iloc[-1] + (2000 * 30)  # Assuming 2000 calories burned per day for a month
    predicted_weight_loss = model.predict([[predicted_calories]])[0]
    
    predicted_weight = initial_weight - (predicted_weight_loss / 7700)  # 7700 calories ~ 1 kg weight loss
    return predicted_weight

def predict_monthly_weights(user_data, age, height):
    # For demonstration, we'll create a simple model assuming weight loss based on calories burned
    # This is a very simplistic approach and not accurate for real-life use
    user_data['Calories Burned'] = user_data['Calories Burned'].astype(float)
    user_data['Cumulative Calories'] = user_data['Calories Burned'].cumsum()
    
    # Features and target
    X = user_data[['Cumulative Calories']]
    y = user_data['Calories Burned']  # Assuming initial weight is proportional to calories burned
    
    # Dummy initial weight
    initial_weight = 70
    
    # Fit model
    model = LinearRegression()
    model.fit(X, y)
    
    # Predict monthly weights
    monthly_weights = []
    for month in range(1, 13):
        predicted_calories = user_data['Cumulative Calories'].iloc[-1] + (2000 * 30 * month)  # Assuming 2000 calories burned per day
        predicted_weight_loss = model.predict([[predicted_calories]])[0]
        predicted_weight = initial_weight - (predicted_weight_loss / 7700)  # 7700 calories ~ 1 kg weight loss
        monthly_weights.append(predicted_weight)
    
    return pd.Series(monthly_weights, index=[f'Month {i}' for i in range(1, 13)])