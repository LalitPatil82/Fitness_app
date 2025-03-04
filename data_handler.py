import pandas as pd
import os

DATA_DIR = 'data'

def get_file_path(user_name):
    return os.path.join(DATA_DIR, f'{user_name}.csv')

def save_activity(user_name, date, activity, duration, calories_burned):
    file_path = get_file_path(user_name)
    data = {
        'Date': [date],
        'Activity': [activity],
        'Duration': [duration],
        'Calories Burned': [calories_burned]
    }
    df = pd.DataFrame(data)
    
    if os.path.exists(file_path):
        existing_df = pd.read_csv(file_path)
        df = pd.concat([existing_df, df], ignore_index=True)
    
    df.to_csv(file_path, index=False)

def load_user_data(user_name):
    file_path = get_file_path(user_name)
    if os.path.exists(file_path):
        return pd.read_csv(file_path)
    else:
        return pd.DataFrame(columns=['Date', 'Activity', 'Duration', 'Calories Burned'])