from google.adk import Agent
from skills.translation_skill import translate_to_nepali

class TranslatorAgent:
    def __init__(self, api_key: str = None):
        self.api_key = api_key
        self.agent = Agent(
            name="nepali_agent",
            model="gemini-1.5-flash",
            instruction=(
                "You are Nepali Language Agent, a translation and localization expert. "
                "Your role is to translate English agricultural reports into simple, polite, "
                "encouraging, and voice-friendly Nepali suited for smallholder farmers."
            )
        )

    def run(self, text: str) -> str:
        """
        Executes the agent logic.
        """
        return translate_to_nepali(text=text, api_key=self.api_key)
