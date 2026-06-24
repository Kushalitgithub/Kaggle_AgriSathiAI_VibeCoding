from fastmcp import FastMCP
import random

mcp = FastMCP("Weather Intelligence Server")

@mcp.tool()
def get_forecast(location: str) -> str:
    """
    Retrieves a 7-day weather forecast for a given location.
    Args:
        location: The town, district, or city name.
    """
    loc_lower = location.lower()
    
    # Regional Nepalese weather adjustments
    if "jhapa" in loc_lower or "birtamod" in loc_lower or "sunsari" in loc_lower or "dharan" in loc_lower:
        region = "Terai Plains (Hot & Humid)"
        temp = "30°C - 33°C"
        humidity = "82% - 90%"
        conditions = "Heavy monsoon rain showers expected over the next 4 days."
    elif "kathmandu" in loc_lower or "lalitpur" in loc_lower or "bhaktapur" in loc_lower:
        region = "Kathmandu Valley (Moderate)"
        temp = "22°C - 26°C"
        humidity = "75% - 85%"
        conditions = "Intermittent light rain showers and cloudy skies."
    elif "kaski" in loc_lower or "pokhara" in loc_lower:
        region = "Pokhara Valley (Very Wet)"
        temp = "24°C - 27°C"
        humidity = "88% - 95%"
        conditions = "Very heavy rain and thunderstorms daily."
    else:
        region = "Hilly/Mountain region"
        temp = "15°C - 20°C"
        humidity = "60% - 70%"
        conditions = "Partly cloudy with mild wind."

    forecast = (
        f"### Weather Forecast for {location} ({region})\n"
        f"- **Current Temp:** {temp}\n"
        f"- **Average Humidity:** {humidity}\n"
        f"- **Outlook:** {conditions}\n"
        f"- **7-Day Trend:** High moisture retention in soil. Rain expected on 5 out of the next 7 days."
    )
    return forecast

@mcp.tool()
def assess_weather_risks(location: str, temperature: float, humidity: float) -> str:
    """
    Evaluates weather risk levels for crop diseases and frost based on temperature and humidity.
    Args:
        location: Farming location.
        temperature: Current or forecasted temperature in Celsius.
        humidity: Current or forecasted relative humidity percentage (0-100).
    """
    risks = []
    recommendation = []
    
    # Late Blight / Fungal disease risk (20-25C, high humidity)
    if 18.0 <= temperature <= 26.0 and humidity >= 80.0:
        risks.append("🔴 **CRITICAL**: High Fungal Disease Spread (e.g., Late Blight in Tomato/Potato). Warm, highly humid environments promote rapid zoospore germination.")
        recommendation.append("Reduce overhead irrigation. Prune lower leaves to allow ventilation. Spray organic copper soap preemptively if symptoms appear nearby.")
    
    # Blast disease in rice (warm, high humidity, wind)
    if 24.0 <= temperature <= 32.0 and humidity >= 85.0:
        risks.append("🔴 **CRITICAL**: High Rice Blast Disease Risk. Spores germinate rapidly in moisture film on leaves.")
        recommendation.append("Monitor rice leaves for spindle-shaped spots. Avoid excessive nitrogen applications.")

    # Frost Risk (low temp)
    if temperature <= 4.0:
        risks.append("🔴 **CRITICAL**: Severe Frost Risk. Can cause cell freezing and leaf necrosis.")
        recommendation.append("Set up light mulching. Perform shallow evening irrigation to increase soil thermal retention. Build temporary windbreaks.")

    # Drought/Heat Stress
    if temperature >= 35.0 and humidity <= 40.0:
        risks.append("🟡 **WARNING**: High Evapotranspiration & Drought Stress.")
        recommendation.append("Apply thick straw mulching to preserve soil moisture. Irrigate in the early morning or late evening. Check soil moisture depth.")

    if not risks:
        risks.append("🟢 **NORMAL**: No immediate weather-triggered disease or frost risks detected.")
        recommendation.append("Maintain regular seasonal watering and crop care schedules.")

    risk_report = (
        f"### Weather Risk Assessment for {location}\n"
        f"**Input Conditions:** {temperature}°C, {humidity}% Humidity\n"
        f"**Identified Risks:**\n" + "\n".join(risks) + "\n\n"
        f"**Irrigation & Farm Action Suggestions:**\n" + "- " + "\n- ".join(recommendation)
    )
    return risk_report

if __name__ == "__main__":
    mcp.run()
