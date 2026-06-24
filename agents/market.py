from google.adk import Agent
from skills.market_forecasting_skill import forecast_market

class MarketAgent:
    def __init__(self, api_key: str = None):
        self.api_key = api_key
        self.agent = Agent(
            name="market_agent",
            model="gemini-1.5-flash",
            instruction=(
                "You are Market Intelligence Agent, a commodity economist. "
                "Your role is to analyze current crop prices, historical price curves, "
                "and recommend optimal sales windows or storage strategies."
            )
        )

    def run(self, crop: str, district: str = "Kathmandu") -> dict:
        """
        Executes the agent logic.
        """
        return forecast_market(crop=crop, district=district)
class_name = "MarketAgent"
