from mcp_servers.weather_mcp import get_forecast, assess_weather_risks

def analyze_weather(location: str, temperature: float = 23.0, humidity: float = 85.0) -> dict:
    """
    Retrieves weather forecast and assesses risk parameters for a farm location.
    
    Returns:
        dict: {
            "forecast": str,
            "risk_report": str,
            "has_warnings": bool
        }
    """
    # 1. Fetch forecast text from weather server
    forecast_text = get_forecast(location)
    
    # 2. Assess risks
    risk_report = assess_weather_risks(location, temperature, humidity)
    
    # Check if there are critical warnings
    has_warnings = "🔴" in risk_report
    
    return {
        "forecast": forecast_text,
        "risk_report": risk_report,
        "has_warnings": has_warnings
    }
