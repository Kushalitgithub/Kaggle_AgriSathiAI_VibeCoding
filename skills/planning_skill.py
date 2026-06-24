def generate_farm_plan(crop: str, condition: str) -> dict:
    """
    Generates a structured weekly milestone task list for crop health recovery or maintenance.
    
    Returns:
        dict: {
            "schedule": list of dicts: {"week": str, "tasks": list of str},
            "milestone": str
        }
    """
    cond_lower = condition.lower()
    crop_title = crop.title()
    
    schedule = []
    
    if "healthy" in cond_lower:
        milestone = "Maintain optimal yield and crop health across the seasonal lifecycle."
        schedule = [
            {
                "week": "Week 1",
                "tasks": [
                    f"Perform routine soil moisture checks (target depth 2-3 inches).",
                    f"Inspect under-leaves for early pest/pathogen indicators.",
                    f"Apply compost/organic fertilizer as scheduled."
                ]
            },
            {
                "week": "Week 2",
                "tasks": [
                    f"Weed the buffer zones around the crop area.",
                    f"Apply preventive organic neem oil foliar spray.",
                    f"Check irrigation emitters for blockages."
                ]
            },
            {
                "week": "Week 3",
                "tasks": [
                    f"Prune excess side-shoots to improve light penetration.",
                    f"Track soil pH and adjust water quality if needed."
                ]
            },
            {
                "week": "Week 4",
                "tasks": [
                    f"Assess overall crop development milestones.",
                    f"Prepare harvest crates and storage spaces."
                ]
            }
        ]
    elif "late blight" in cond_lower or "early blight" in cond_lower or "blast" in cond_lower:
        # Fungal diseases
        milestone = "Eradicate fungal pathogen spread and restore plant vascular vigor."
        schedule = [
            {
                "week": "Week 1 (Containment)",
                "tasks": [
                    f"Remove and safely burn or bury infected leaves (do NOT compost).",
                    f"Apply copper octanoate (organic) or Metalaxyl fungicide immediately.",
                    f"Suspend overhead sprinkler irrigation; switch to base/drip watering."
                ]
            },
            {
                "week": "Week 2 (Foliar Care)",
                "tasks": [
                    f"Prune bottom leaves (lower 12 inches) to maximize air circulation.",
                    f"Apply a second protective fungicide spray (organic or chemical).",
                    f"Clean and sanitize all pruning shears with 10% bleach solution."
                ]
            },
            {
                "week": "Week 3 (Nutrition Support)",
                "tasks": [
                    f"Apply potassium and calcium foliar fertilizer to strengthen crop cell walls.",
                    f"Avoid high nitrogen applications (excess nitrogen promotes lush, blight-susceptible growth).",
                    f"Inspect neighboring rows for secondary infection indicators."
                ]
            },
            {
                "week": "Week 4 (Evaluation)",
                "tasks": [
                    f"Confirm if new vegetative growth is spot-free.",
                    f"Map out next year's crop rotation plan (rotate with non-solanaceous/blast-resistant plants).",
                    f"Establish grass/mulch barrier underneath plants to prevent soil spore splash."
                ]
            }
        ]
    elif "stem borer" in cond_lower or "pest" in cond_lower:
        # Pests
        milestone = "Eradicate pest population and protect reproductive tillers/shoots."
        schedule = [
            {
                "week": "Week 1 (Pest Control)",
                "tasks": [
                    f"Deploy light traps (1 trap per 0.5 hectares) to capture adult moths.",
                    f"Release egg parasite Trichogramma wasps.",
                    f"Apply systemic insecticide (Cartap or organic equivalent) to standing water if threshold exceeded."
                ]
            },
            {
                "week": "Week 2 (Monitoring)",
                "tasks": [
                    f"Walk the field daily to record percentages of 'dead hearts' or wilted stems.",
                    f"Clear broadleaf weeds around borders which serve as pest nesting sites."
                ]
            },
            {
                "week": "Week 3 (Crop Recovery)",
                "tasks": [
                    f"Apply a urea/compost side-dress to encourage tiller recovery.",
                    f"Maintain stable water depth (approx 5cm) to suppress pest movement."
                ]
            },
            {
                "week": "Week 4 (Assessment)",
                "tasks": [
                    f"Confirm stem borer larval count is below economic threshold.",
                    f"Harvest crop close to ground level during harvest week to eliminate larvae overwintering in stubble."
                ]
            }
        ]
    else:
        # Default / Bacterial Wilt
        milestone = "Contain bacterial spread and sanitize farm plots."
        schedule = [
            {
                "week": "Week 1 (Isolation)",
                "tasks": [
                    f"Uproot and burn infected plants. Do not touch healthy plants after touching diseased ones.",
                    f"Drench infected soil pockets with copper oxychloride solution to sanitize.",
                    f"Create soil runoff channels to prevent contaminated water from flowing to healthy fields."
                ]
            },
            {
                "week": "Week 2 (Tool Sanitation)",
                "tasks": [
                    f"Sterilize all spades, hoes, boots, and gloves after working in the infected plot.",
                    f"Erect isolation fencing around infected soil zones."
                ]
            },
            {
                "week": "Week 3 (Field Rest)",
                "tasks": [
                    f"Apply lime to soil to raise pH, making it less favorable for bacteria.",
                    f"Fallow the infected plot or plant non-host crops (e.g. maize, wheat) in adjacent zones."
                ]
            },
            {
                "week": "Week 4 (Future Planning)",
                "tasks": [
                    f"Acquire certified disease-free seeds/tubers for the next cycle.",
                    f"Establish a 3 to 5 year crop rotation system for this plot."
                ]
            }
        ]

    return {
        "schedule": schedule,
        "milestone": milestone,
        "crop": crop_title,
        "condition": condition
    }
