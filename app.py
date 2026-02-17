import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils.data_loader import load_data
from utils.forecasting import train_and_forecast, load_model
from utils.optimization import optimize_energy
from utils.recommendation import generate_recommendation

# Page Configuration
st.set_page_config(
    page_title="Energy AI Dashboard",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
    <style>
    .main {
        background-color: #f5f7f9;
    }
    .stMetric {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 5px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .stCard {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    h1, h2, h3 {
        color: #0e2a47; 
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar Navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", 
    ["Executive Summary", "Energy Trends & Forecast", "Optimization Simulator", "Strategic Scenario Analysis"])

# Load Data
@st.cache_data
def get_data():
    return load_data()

df = get_data()

# Global Calculations
total_energy = df['energy_consumption_kwh'].sum()
total_cost = df['total_cost'].sum()
total_emissions = df['total_emission'].sum()

# Helper: Forecast Logic
# We run forecast only if needed or cached
@st.cache_resource
def get_forecast(data):
    return train_and_forecast(data)

forecast_df, mae = get_forecast(df)

# Page 1: Executive Summary
if page == "Executive Summary":
    st.title("⚡ Executive Energy Dashboard")
    st.markdown("### High-Level KPI Overview (YTD)")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(label="Total Energy (kWh)", value=f"{total_energy/1000:,.1f} MWh", delta="2.4%")
    
    with col2:
        st.metric(label="Total Cost", value=f"${total_cost:,.0f}", delta="-1.2%")
        
    with col3:
        st.metric(label="Total Emissions", value=f"{total_emissions:,.1f} Tons", delta="0.5%", delta_color="inverse")
        
    with col4:
        # Forecast for next month
        next_month_forecast = forecast_df.iloc[0]['energy_consumption_kwh'] if not forecast_df.empty else 0
        st.metric(label="Next Month Forecast", value=f"{next_month_forecast:,.0f} kWh")

    st.markdown("---")
    
    # Trends Visualization
    st.subheader("Energy Consumption Trends")
    fig = px.line(df, x='date', y='energy_consumption_kwh', title='Historical Energy Consumption')
    fig.update_layout(height=400, template='plotly_white')
    st.plotly_chart(fig, use_container_width=True)

# Page 2: Energy Trends & Forecast
elif page == "Energy Trends & Forecast":
    st.title("📈 Energy Trends & AI Forecast")
    
    st.markdown(f"**Model Performance (MAE):** {mae:.2f} kWh")
    
    # Checkbox to show historical data
    show_history = st.checkbox("Show Historical Data", value=True)
    
    # Combine historical and forecast for plotting
    historical_plot = df[['date', 'energy_consumption_kwh']].copy()
    historical_plot['Type'] = 'Historical'
    
    forecast_plot = forecast_df[['date', 'energy_consumption_kwh']].copy()
    forecast_plot['Type'] = 'Forecast'
    
    combined_df = pd.concat([historical_plot, forecast_plot])
    
    if not show_history:
        combined_df = combined_df[combined_df['Type'] == 'Forecast']
    
    fig_forecast = px.line(combined_df, x='date', y='energy_consumption_kwh', color='Type', 
                           title='Energy Consumption Forecast (Next 3 Months)',
                           color_discrete_map={"Historical": "#1f77b4", "Forecast": "#ff7f0e"})
    
    # Add confidence interval (simulated for visual effect since RF doesn't give it directly mostly)
    # Actually, let's keep it simple line chart as per requirements.
    
    st.plotly_chart(fig_forecast, use_container_width=True)
    
    st.subheader("Forecast Data")
    st.dataframe(forecast_df)

# Page 3: Optimization Simulator
elif page == "Optimization Simulator":
    st.title("🛠️ Optimization Simulator")
    
    col_sim_1, col_sim_2 = st.columns([1, 2])
    
    with col_sim_1:
        st.markdown("### Configuration")
        strategy = st.selectbox("Select Strategy", 
                                ["Peak Hour Optimization", "Renewable Integration", "Efficiency Upgrade"])
        
        reduction_pct = st.slider("Target Energy Reduction (%)", min_value=1, max_value=50, value=10)
        
        # Calculate
        # We need annual metrics basically, let's use the sum of total data as 'Annual' proxy or last 12 months.
        # Let's use last 12 months for calculation to be realistic.
        last_12m = df.tail(12)
        annual_energy = last_12m['energy_consumption_kwh'].sum()
        annual_cost = last_12m['total_cost'].sum()
        annual_emissions = last_12m['total_emission'].sum()
        
        results = optimize_energy(annual_energy, annual_cost, annual_emissions, reduction_pct, strategy)
        
        st.success("Simulation Complete")
    
    with col_sim_2:
        st.markdown(f"### Projected Impact: {strategy}")
        
        # Comparison Metrics
        c1, c2, c3 = st.columns(3)
        c1.metric("New Energy (Annual)", f"{results['new_energy']/1000:,.1f} MWh", 
                  f"-{reduction_pct}%", delta_color="inverse")
        c2.metric("Projected Savings", f"${results['annual_savings']:,.0f}", 
                  "Savings")
        c3.metric("ROI / Payback", f"{results['roi']:.1f} Years" if strategy == "Renewable Integration" else "N/A")
        
        # Visual Comparison
        comparison_data = pd.DataFrame({
            'Metric': ['Energy (MWh)', 'Cost ($)', 'Emissions (Tons)'],
            'Baseline': [annual_energy/1000, annual_cost, annual_emissions],
            'Optimized': [results['new_energy']/1000, results['new_cost'], results['new_emissions']]
        })
        
        cutoff = st.radio("Visualize Metric", ['Energy', 'Cost', 'Emissions'])
        
        if cutoff == 'Energy':
            y_val = ['Baseline', 'Optimized']
            x_val = [annual_energy/1000, results['new_energy']/1000]
            title = "Annual Energy Consumption (MWh)"
        elif cutoff == 'Cost':
            y_val = ['Baseline', 'Optimized']
            x_val = [annual_cost, results['new_cost']]
            title = "Annual Operational Cost ($)"
        else:
            y_val = ['Baseline', 'Optimized']
            x_val = [annual_emissions, results['new_emissions']]
            title = "Annual CO2 Emissions (Tons)"
            
        fig_bar = go.Figure(data=[
            go.Bar(name='Baseline', x=['Baseline'], y=[x_val[0]], marker_color='#1f77b4'),
            go.Bar(name='Optimized', x=['Optimized'], y=[x_val[1]], marker_color='#2ca02c')
        ])
        fig_bar.update_layout(title=title)
        st.plotly_chart(fig_bar, use_container_width=True)

# Page 4: Strategic Scenario Analysis
elif page == "Strategic Scenario Analysis":
    st.title("🧐 Strategic Scenario Analysis")
    
    st.markdown("### AI-Generated Recommendation")
    
    # Calculate trends for recommendation logic
    # Cost trend MoM (last month vs previous)
    if len(df) >= 2:
        last_month_cost = df.iloc[-1]['total_cost']
        prev_month_cost = df.iloc[-2]['total_cost']
        cost_trend_pct = ((last_month_cost - prev_month_cost) / prev_month_cost) * 100
    else:
        cost_trend_pct = 0
        
    # Emission level heuristic
    avg_annual_emission = df['total_emission'].mean() * 12
    # Just a placeholder check
    emission_level = "High" if df.iloc[-1]['total_emission'] > df['total_emission'].mean() else "Normal"
    
    rec_text, strategy_sugg = generate_recommendation(cost_trend_pct, emission_level)
    
    st.info(rec_text)
    
    st.markdown("### Scenario Comparison")
    
    # Create a table comparing 3 scenarios
    scenarios = []
    
    # Base
    last_12m = df.tail(12)
    base_energy = last_12m['energy_consumption_kwh'].sum()
    base_cost = last_12m['total_cost'].sum()
    
    strategies = ["Efficiency Upgrade", "Renewable Integration", "Peak Hour Optimization"]
    reductions = [15, 25, 10] # Hypothesized impact
    
    for s, r in zip(strategies, reductions):
        res = optimize_energy(base_energy, base_cost, 0, r, s) # emissions 0 for simplicity in table
        scenarios.append({
            "Strategy": s,
            "Reduction (%)": r,
            "Annual Savings ($)": res['annual_savings'],
            "New Cost ($)": res['new_cost']
        })
        
    st.table(pd.DataFrame(scenarios))
