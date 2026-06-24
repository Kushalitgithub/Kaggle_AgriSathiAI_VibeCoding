from google.adk import Agent

class FertilizerAgent:
    def __init__(self, api_key: str = None):
        self.api_key = api_key
        self.agent = Agent(
            name="fertilizer_agent",
            model="gemini-1.5-flash",
            instruction=(
                "You are Fertilizer Advisor, a plant nutrition expert. "
                "Your role is to diagnose nutrient deficiencies, specify balanced N-P-K schedules, "
                "and recommend eco-friendly, organic alternatives to prevent soil degradation."
            )
        )

    def run(self, crop: str, condition: str) -> dict:
        """
        Generates fertilizer schedule recommendations based on crop health state.
        """
        crop_lower = crop.lower()
        cond_lower = condition.lower()
        
        schedule = ""
        alternatives = ""
        deficiency_warning = ""
        
        if "healthy" in cond_lower:
            deficiency_warning = "🟢 No severe nutrient deficiencies detected."
            schedule = (
                "Apply basic well-rotted farmyard manure (FYM) or compost at 10 tons/hectare. "
                "Maintain nitrogen-phosphorus-potassium (N-P-K) split applications at standard vegetative rates."
            )
            alternatives = "Use vermicompost, bone meal for phosphorus, and wood ash for potassium to avoid chemical reliance."
        elif "blight" in cond_lower:
            deficiency_warning = "🟡 Possible Calcium (Ca) restriction due to water-soaked fungal lesions."
            schedule = (
                "❌ DO NOT apply excessive Nitrogen (urea) as it causes lush, watery vegetative growth highly vulnerable to blight.\n"
                "✔️ Apply Calcium Nitrate (0.5% foliar spray) to strengthen plant cell walls.\n"
                "✔️ Apply Potassium Sulfate to improve leaf tissue disease resistance."
            )
            alternatives = "Drench soil with liquid seaweed extract or compost tea to introduce beneficial microbes that compete with blight spores."
        elif "blast" in cond_lower:
            deficiency_warning = "🟡 Silicon (Si) and Potassium (K) deficiency makes plants susceptible to fungal blast penetration."
            schedule = (
                "❌ Reduce top-dressed urea application.\n"
                "✔️ Apply Potassium Chloride (MOP) at 50 kg/hectare during the tillering stage.\n"
                "✔️ Apply Calcium Silicate slag to raise silicon levels, providing physical leaf resistance against blast spores."
            )
            alternatives = "Incorporate bio-fertilizers like Azotobacter and apply carbonized rice husk (rich in silicon) to the soil."
        else:
            deficiency_warning = "⚠️ General nutrient stress detected due to pathogen load."
            schedule = (
                "Provide balanced foliar N-P-K spray (19-19-19) at 2g/liter of water to bypass damaged roots. "
                "Apply gypsum to the soil to supply sulfur and calcium."
            )
            alternatives = "Apply poultry manure tea or diluted biogas slurry as a light foliar spray to promote recovery."
            
        return {
            "crop": crop,
            "condition": condition,
            "deficiency_warning": deficiency_warning,
            "schedule": schedule,
            "organic_alternatives": alternatives
        }
