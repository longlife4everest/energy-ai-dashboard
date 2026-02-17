def generate_recommendation(cost_trend_pct, emission_level, renewable_share=0):
    """
    Generate executive strategic recommendation based on trends.
    
    Rules:
    - If emissions high (> threshold) -> recommend efficiency
    - If cost rising > 5% MoM -> recommend peak optimization
    - If both -> recommend renewable integration
    """
    
    # Define thresholds
    # Assuming emission_level is annual tons or similar logic
    # We can use qualitative checks since we don't have hard thresholds in prompt except "high"
    # Let's assume input 'emission_level' is a string label or we infer "high" from data context in app.py.
    # Actually, simpler: pass boolean flags or raw values.
    
    recommendation_text = ""
    strategy_suggestion = ""
    
    is_high_emissions = False
    is_cost_rising = False
    
    if cost_trend_pct > 5.0:
        is_cost_rising = True
        
    # We'll need a heuristic for "high emissions". 
    # Maybe if emissions didn't decrease or are above average?
    # Let's pass a boolean 'is_high_emissions' to this function to keep logic clean, 
    # or handle the logic inside app.py and pass the result here.
    # But this is the "engine".
    # Let's assume emission_level is "High", "Medium", "Low" string for now.
    
    if emission_level == "High":
        is_high_emissions = True
        
    if is_high_emissions and is_cost_rising:
        recommendation_text = (
            "**Critical Strategic Pivot Required:** Both operational costs and carbon emissions are statistically elevated. "
            "Immediate intervention recommended: **Renewable Energy Integration**. "
            "This strategy addresses both fiscal efficiency and sustainability targets simultaneously."
        )
        strategy_suggestion = "Renewable Integration"
        
    elif is_cost_rising:
        recommendation_text = (
            "**Cost Contaminment Alert:** Energy expenditures are trending upwards (>5% MoM). "
            "Recommended Action: **Peak Hour Load Shifting**. "
            "Optimizing consumption during non-peak tariff periods will stabilize operational significantly expenses."
        )
        strategy_suggestion = "Peak Hour Optimization"
        
    elif is_high_emissions:
        recommendation_text = (
            "**Sustainability Target Risk:** Carbon footprint indicators are above nominal thresholds. "
            "Recommended Action: **Infrastructure Efficiency Upgrades**. "
            "Modernizing equipment will directly reduce KWh consumption and associated emissions."
        )
        strategy_suggestion = "Efficiency Upgrade"
        
    else:
        recommendation_text = (
            "**Operations Nominal:** Energy consumption and costs are within expected variance. "
            "Recommendation: Maintain current monitoring protocols and evaluate long-term **Renewable Integration** for future-proofing."
        )
        strategy_suggestion = "Monitor"
        
    return recommendation_text, strategy_suggestion
