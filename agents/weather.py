from google.adk import Agent
from skills.weather_analysis_skill import analyze_weather

class WeatherAgent:
    def __init__(self, api_key: str = None):
        self.api_key = api_key
        self.agent = Agent(
            name="weather_agent",
            model="gemini-1.5-flash",
            instruction=(
                "You are Weather Intelligence Agent, a meteorological agricultural advisor. "
                "Your role is to assess weather forecasts, evaluate disease risk parameters, and suggest irrigation adjustments."
            )
        )

    def run(self, location: str, temp: float = 23.0, humidity: float = 85.0) -> dict:
        """
        Executes the agent logic.
        """
        return analyze_weather(location=location, temperature=temp, humidity=humidity)
