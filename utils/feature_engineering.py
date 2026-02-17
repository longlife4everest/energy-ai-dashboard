import pandas as pd

def create_features(df):
    """
    Create time-based features for forecasting.
    Input: DataFrame with 'date' and 'energy_consumption_kwh'.
    Output: DataFrame with new features.
    """
    df = df.copy()
    
    # Ensure date is datetime
    df['date'] = pd.to_datetime(df['date'])
    
    # Time features
    df['month'] = df['date'].dt.month
    df['year'] = df['date'].dt.year
    
    # Lag features (Energy use from 1 month ago)
    df['lag_1m'] = df['energy_consumption_kwh'].shift(1)
    
    # Rolling mean (3-month moving average)
    df['rolling_mean_3m'] = df['energy_consumption_kwh'].rolling(window=3).mean()
    
    # Drop rows with NaN created by lag/rolling (first few rows)
    # For training we need clean data.
    # However, for the very latest data point we might not want to drop if we are predicting.
    # But this function is likely used before training.
    
    return df
