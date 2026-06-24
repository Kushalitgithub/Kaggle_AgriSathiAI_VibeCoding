from google.adk import Agent
from agents.crop_doctor import CropDoctor
from agents.weather import WeatherAgent
from agents.fertilizer import FertilizerAgent
from agents.market import MarketAgent
from agents.planner import PlannerAgent
from agents.translator import TranslatorAgent

from skills.summarization_skill import summarize_recommendations
from skills.report_skill import compile_farm_report
from security.audit_logger import log_event

class Orchestrator:
    def __init__(self, api_key: str = None):
        self.api_key = api_key
        # Initialize ADK Orchestrator Agent
        self.agent = Agent(
            name="orchestrator",
            model="gemini-1.5-flash",
            instruction=(
                "You are AgriSathi Orchestrator, the central coordinator of the multi-agent agricultural system. "
                "Your role is to receive farmer inquiries, invoke specialized agents (Crop Doctor, Weather, "
                "Fertilizer, Market, Planner, Translator) in sequence, maintain conversation memory, "
                "and compile the consolidated results into a comprehensive farmer advice document."
            )
        )
        
        # Instantiate sub-agents
        self.crop_doctor = CropDoctor(api_key=api_key)
        self.weather_agent = WeatherAgent(api_key=api_key)
        self.fertilizer_agent = FertilizerAgent(api_key=api_key)
        self.market_agent = MarketAgent(api_key=api_key)
        self.planner_agent = PlannerAgent(api_key=api_key)
        self.translator_agent = TranslatorAgent(api_key=api_key)
        
        # Session conversation memory
        self.memory = []

    def execute_antigravity_workflow(self, image_path: str = None, symptoms_text: str = "", location: str = "Kathmandu", user: str = "farmer_1", role: str = "Farmer") -> dict:
        """
        Coordinates the full autonomous agent chain:
        Image Upload -> Crop Doctor -> Weather Agent -> Fertilizer Agent -> Market Agent -> Farm Planner -> Nepali Translator.
        """
        log_event(user=user, role=role, action="ANTIGRAVITY_WORKFLOW_START", details=f"Initiating agent chain with image={image_path}, symptoms={symptoms_text}")
        
        # 1. Crop Doctor Analysis
        diag_output = self.crop_doctor.run(image_path=image_path, symptoms_text=symptoms_text)
        crop = diag_output.get("crop", "Tomato")
        condition = diag_output.get("condition", "Late Blight")
        
        # 2. Weather Assessment
        # Assume typical values or retrieve from location. Let's adjust inputs based on crop
        temp = 22.0 if "blight" in condition.lower() else (28.0 if "blast" in condition.lower() else 25.0)
        humidity = 88.0 if ("blight" in condition.lower() or "blast" in condition.lower()) else 65.0
        weather_output = self.weather_agent.run(location=location, temp=temp, humidity=humidity)
        
        # 3. Fertilizer Schedule Evaluation
        fertilizer_output = self.fertilizer_agent.run(crop=crop, condition=condition)
        
        # 4. Market Opportunity Analysis
        market_output = self.market_agent.run(crop=crop, district=location)
        
        # 5. Farm Calendaring & Action Plan
        plan_output = self.planner_agent.run(crop=crop, condition=condition)
        
        # 6. Synthesize Executive English Summary
        summary_text = summarize_recommendations(
            diagnostics=diag_output,
            weather=weather_output,
            market=market_output,
            plan=plan_output
        )
        
        # 7. Nepali Language Localizer
        nepali_translation = self.translator_agent.run(text=summary_text)
        
        # 8. Compile Comprehensive Report
        final_report = compile_farm_report(
            diagnostics=diag_output,
            weather=weather_output,
            market=market_output,
            plan=plan_output,
            nepali_translation=nepali_translation
        )
        
        # Save to memory
        workflow_session = {
            "query": f"Diagnose {crop} crop health in {location}",
            "diagnostics": diag_output,
            "weather": weather_output,
            "fertilizer": fertilizer_output,
            "market": market_output,
            "plan": plan_output,
            "summary": summary_text,
            "nepali_translation": nepali_translation,
            "final_report": final_report
        }
        self.memory.append(workflow_session)
        
        log_event(
            user=user,
            role=role,
            action="ANTIGRAVITY_WORKFLOW_COMPLETE",
            details=f"Completed agent chain. Diagnosed: {crop} ({condition}) in {location}.",
            status="SUCCESS"
        )
        
        return workflow_session
