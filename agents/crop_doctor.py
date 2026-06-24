from google.adk import Agent
from skills.diagnosis_skill import run_diagnosis

class CropDoctor:
    def __init__(self, api_key: str = None):
        self.api_key = api_key
        # We define the ADK agent
        self.agent = Agent(
            name="crop_doctor",
            model="gemini-1.5-flash",
            instruction=(
                "You are Crop Doctor, a plant pathologist assistant. "
                "Your role is to diagnose crop conditions, identify pathogens, and specify "
                "detailed organic and chemical treatment plans."
            )
        )

    def run(self, image_path: str = None, symptoms_text: str = "") -> dict:
        """
        Executes the agent logic by invoking the diagnosis skill.
        """
        return run_diagnosis(image_path=image_path, symptoms_text=symptoms_text, api_key=self.api_key)
