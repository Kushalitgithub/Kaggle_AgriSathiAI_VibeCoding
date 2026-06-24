def compile_farm_report(diagnostics: dict, weather: dict, market: dict, plan: dict, nepali_translation: str) -> str:
    """
    Compiles all agent outputs into a structured, printable agricultural report.
    """
    crop = diagnostics.get("crop", "Crop").title()
    condition = diagnostics.get("condition", "Condition").title()
    confidence = diagnostics.get("confidence", 0.8) * 100
    
    report = f"""# AGRISATHI AI - COMPREHENSIVE FARM INTELLIGENCE REPORT
**Generating Timestamp:** 2026-06-24 18:00 (NPT)
**Platform Core Version:** v2.0-Prod

---

## 1. CROP DIAGNOSTIC REPORT (Crop Doctor Agent)
- **Target Crop:** {crop}
- **Detected Condition:** {condition}
- **Detection Confidence:** {confidence:.1f}%
- **Identified Symptoms:** 
  {diagnostics.get("symptoms", "No visual symptoms found.")}

### Treatment Protocols:
- **Organic Intervention:** 
  {diagnostics.get("organic_treatment", "N/A")}
- **Chemical Control:** 
  {diagnostics.get("chemical_treatment", "N/A")}
- **Long-term Prevention:** 
  {diagnostics.get("preventative_measures", "N/A")}

---

## 2. METEOROLOGICAL RISK ANALYSIS (Weather Agent)
{weather.get("forecast", "No forecast data.")}

{weather.get("risk_report", "No risk analysis.")}

---

## 3. ECONOMIC OPPORTUNITY FORECAST (Market Agent)
{market.get("current_prices", "No pricing data.")}

{market.get("trends", "No trend data.")}

---

## 4. FARM CALENDAR & RECOVERY PLAN (Farm Planner Agent)
**Recovery Objective / Milestone:** {plan.get("milestone", "Optimize crop growth.")}

"""
    # Append the weekly schedules
    for wk in plan.get("schedule", []):
        report += f"### {wk['week']}\n"
        for task in wk["tasks"]:
            report += f"- [ ] {task}\n"
        report += "\n"
        
    report += f"""---

## 5. LOCAL LANGUAGE TRANSLATION (Nepali Agent)
{nepali_translation}

---
*Report generated autonomously by AgriSathi AI Multi-Agent Coordinator.*
"""
    return report
