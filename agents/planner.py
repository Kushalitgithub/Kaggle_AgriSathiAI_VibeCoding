from google.adk import Agent
from skills.planning_skill import generate_farm_plan

class PlannerAgent:
    def __init__(self, api_key: str = None):
        self.api_key = api_key
        self.agent = Agent(
            name="planner_agent",
            model="gemini-1.5-flash",
            instruction=(
                "You are Farm Planner, a scheduling and operations specialist. "
                "Your role is to design detailed task lists, recovery schedules, "
                "and crop management calendars to structure farm labor effectively."
            )
        )

    def run(self, crop: str, condition: str) -> dict:
        """
        Executes the agent logic.
        """
        return generate_farm_plan(crop=crop, condition=condition)
