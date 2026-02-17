def optimize_energy(current_annual_energy, current_annual_cost, current_annual_emissions, reduction_pct, strategy_type):
    """
    Calculate new metrics based on reduction percentage and strategy.
    Strategies:
    - Peak Hour Optimization
    - Renewable Integration
    - Efficiency Upgrade
    """
    
    savings_factor = reduction_pct / 100.0
    
    # Baseline calculations
    new_energy = current_annual_energy * (1 - savings_factor)
    new_cost = current_annual_cost * (1 - savings_factor) # Assuming linear cost reduction for simplicity unless strategy differs
    new_emissions = current_annual_emissions * (1 - savings_factor)
    
    annual_savings = current_annual_cost - new_cost
    roi = 0.0
    investment = 0.0
    
    # Strategy specific adjustments
    if strategy_type == "Renewable Integration":
        # User req: Assume fixed investment cost = 50000
        investment = 50000
        if annual_savings > 0:
            roi = (annual_savings / investment) * 100 # ROI % per year? Or standard ROI = (Net Return / Cost)
            # User formula: ROI = investment / annual_savings (This is Payback Period, not ROI).
            # "ROI = investment / annual_savings" -> This results in Years to Payback.
            # Usually ROI = (Gain - Cost) / Cost.
            # But I will follow the user's specific formula instructions if explicit.
            # Prompt says: "ROI = investment / annual_savings"
            # Wait, that calculates "Years".
            # I will label it as "Payback Period (Years)" or just "ROI metric" as requested.
            # If the user insists on ROI, I might clarify or just output the number.
            # Let's calculate Payback Period as requested but maybe label it clearly or reciprocate if they meant ROI %.
            # If investment = 50000, savings = 10000. 50000/10000 = 5.
            # If they meant ROI (Return on Investment), it's usually (Savings/Investment).
            # I will implement as written: investment / annual_savings, but I'll return it as 'roi_years'.
            
            roi = investment / annual_savings if annual_savings != 0 else 0
            
    elif strategy_type == "Efficiency Upgrade":
        # Maybe assumes some investment too? 
        # Requirement didn't specify investment for Efficiency, only Renewable.
        # But usually Efficiency costs money.
        # I'll assume 0 investment if not specified, or add a placeholder.
        # Let's stick to requirements: "If renewable selected: Assume fixed investment..."
        pass
        
    elif strategy_type == "Peak Hour Optimization":
        # Might reduce cost more than energy if peak rates are high.
        # But requirements say: "new_cost = new_energy * cost_per_kwh"
        # So cost reduces linearly with energy in this simplified model.
        pass

    return {
        "new_energy": new_energy,
        "new_cost": new_cost,
        "new_emissions": new_emissions,
        "annual_savings": annual_savings,
        "roi": roi,
        "investment": investment
    }
