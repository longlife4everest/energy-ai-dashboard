# AI-Powered Energy Optimization & Decision Support Dashboard

## Overview
This is a management-grade prototype designed for energy executives (e.g., BP energy managers). It provides an interactive dashboard to monitor energy consumption trends, forecast future usage using AI, simulate optimization strategies, and receive strategic recommendations.

## Features
- **Executive Summary**: High-level KPIs for Energy, Cost, and Emissions.
- **AI Forecasting**: Uses a Random Forest Regressor to predict the next 3 months of energy consumption.
- **Optimization Simulator**: Interactive tool to simulate the impact of various energy reduction strategies (Peak Hour Optimization, Renewable Integration, Efficiency Upgrade).
- **Strategic Recommendations**: Rule-based engine that suggests actionable strategies based on real-time data trends.

## Tech Stack
- **Python**: Core language.
- **Streamlit**: Web application framework.
- **Pandas & NumPy**: Data manipulation and numerical operations.
- **Scikit-learn**: Machine learning for forecasting.
- **Plotly**: Interactive visualizations.
- **Joblib**: Model persistence.

## Installation
1. Clone the repository or extract the project files.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
Run the application using Streamlit:
```bash
streamlit run app.py
```

## Methodology
- **Synthetic Data**: Generates realistic energy data with seasonality, trends, and noise if no source file is provided.
- **Forecasting**: Features include 3-month rolling averages and 1-month lags. The model is retrained on the full dataset before forecasting.
- **Optimization**: Calculates ROI and savings based on reduction targets and specific strategy parameters (e.g., fixed investment for renewables).

## Future Improvements
- Integration with live IoT sensor data.
- Advanced Deep Learning models (LSTM/Prophet) for forecasting.
- More granular calibration of optimization parameters.
