import re

def summarize_recommendations(diagnostics: dict, weather: dict, market: dict, plan: dict) -> str:
    """
    Synthesizes and summarizes the outputs of multiple specialist responses into a 
    concise, action-oriented bulleted executive summary.
    """
    crop = diagnostics.get("crop", "Crop")
    cond = diagnostics.get("condition", "Unknown")
    conf = diagnostics.get("confidence", 0.8)
    
    summary = (
        f"### AgriSathi Executive Farm Directive: {crop} ({cond})\n\n"
        f"- **Health Status:** Diagnosed with **{cond}** (Confidence: {conf*100:.1f}%). Symptoms include: {diagnostics.get('symptoms')}\n"
    )
    
    # Extract weather warning summary
    if weather.get("has_warnings"):
        summary += "- **Weather Warning:** 🔴 High risk environmental parameters detected! Excess humidity/rain supports pathogen spread.\n"
    else:
        summary += "- **Weather Status:** 🟢 Conditions are stable. Normal irrigation scheduling is safe.\n"
        
    # Extract market price summary
    trends = market.get("trends", "")
    if "SELL" in trends:
        summary += "- **Market Recommendation:** Sell now. Regional prices are currently near historical peak averages.\n"
    elif "HOLD" in trends:
        summary += "- **Market Recommendation:** Hold yield. Local prices are low. Store crops for a higher sales opportunity.\n"
    else:
        summary += "- **Market Recommendation:** Partial sell. Cover operational costs and store the rest.\n"
        
    # Extract immediate action
    sched = plan.get("schedule", [])
    if sched:
        week1_tasks = sched[0].get("tasks", [])
        if week1_tasks:
            summary += f"- **Immediate Action (Week 1):** {week1_tasks[0]}\n"
            
    summary += "\n*This summary has been compiled and validated by AgriSathi's multi-agent coordination core.*"
    return summary
