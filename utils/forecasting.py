import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split
import joblib
import os
from .feature_engineering import create_features

MODEL_PATH = 'models/forecast_model.pkl'

def train_and_forecast(df):
    """
    Train a Random Forest model and forecast the next 3 months.
    """
    # Create models directory if not exists
    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    
    # 1. Feature Engineering
    df_features = create_features(df)
    
    # Drop rows with NaN (from lag/rolling)
    df_clean = df_features.dropna()
    
    # Define features and target
    features = ['month', 'year', 'lag_1m', 'rolling_mean_3m']
    target = 'energy_consumption_kwh'
    
    X = df_clean[features]
    y = df_clean[target]
    
    # Robust check for enough data
    if len(X) < 10:
        return None, 0.0
    
    # Split for validation (last 3 months as test set for MAE calculation)
    # But for final forecasting, we should retrain on all data?
    # User requirement: "Calculate MAE" and "Predict next 3 months".
    # Typically: Train/Test split -> Calculate MAE -> Retrain on all -> Forecast.
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)
    
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    predictions = model.predict(X_test)
    mae = mean_absolute_error(y_test, predictions)
    
    # Retrain on full dataset for future forecasting
    model.fit(X, y)
    
    # Save model
    joblib.dump(model, MODEL_PATH)
    
    # Forecast next 3 months
    future_forecast = []
    last_row = df_features.iloc[-1].copy()
    
    current_date = last_row['date']
    
    # Iterative forecasting
    # We need to update lag and rolling mean for each step
    # This involves appending the predicted value to history to calculate next features
    
    history_energy = list(df['energy_consumption_kwh'].values)
    
    for i in range(3):
        next_date = current_date + pd.DateOffset(months=1)
        
        # Calculate features for next date
        lag_1m = history_energy[-1]
        rolling_mean_3m = np.mean(history_energy[-3:])
        
        features_dict = {
            'month': [next_date.month],
            'year': [next_date.year],
            'lag_1m': [lag_1m],
            'rolling_mean_3m': [rolling_mean_3m]
        }
        
        X_future = pd.DataFrame(features_dict)
        pred_energy = model.predict(X_future)[0]
        
        future_forecast.append({
            'date': next_date,
            'energy_consumption_kwh': pred_energy,
            'forecast': True
        })
        
        # Update history
        history_energy.append(pred_energy)
        current_date = next_date
        
    return pd.DataFrame(future_forecast), mae

def load_model():
    if os.path.exists(MODEL_PATH):
        return joblib.load(MODEL_PATH)
    return None
