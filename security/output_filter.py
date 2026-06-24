from security.audit_logger import log_event

# List of banned/highly restricted pesticides in Nepal and globally
BANNED_PESTICIDES = [
    "aldrin", "dieldrin", "endrin", "heptachlor", "chlordane", 
    "mirex", "toxaphene", "hexachlorobenzene", "monocrotophos", 
    "paraquat", "endosulfan", "ddt", "lindane", "methyl parathion"
]

CHEMICAL_FUNGICIDES = [
    "chlorothalonil", "mancozeb", "metalaxyl", "tricyclazole", 
    "azoxystrobin", "isoprothiolane", "copper oxychloride", "bordeaux"
]

CHEMICAL_SAFETY_DISCLAIMER = (
    "\n\n**⚠️ CHEMICAL SAFETY WARNING:** *Always wear protective clothing, gloves, "
    "and masks when handling or spraying chemical products. Maintain recommended dosage rates, "
    "and ensure a safe harvest interval (PHI) before consuming crops. Consult your local "
    "agricultural extension office for local regulations.*"
)

def filter_agent_output(agent_response: str, user: str, role: str) -> str:
    """
    Scans the response for banned pesticides or dangerous recommendations.
    Appends a safety disclaimer if chemical fungicides or pesticides are suggested.
    """
    if not agent_response:
        return agent_response
        
    lower_response = agent_response.lower()
    
    # 1. Check for banned pesticides
    for pesticide in BANNED_PESTICIDES:
        if pesticide in lower_response:
            log_event(
                user=user,
                role=role,
                action="BANNED_SUBSTANCE_DETECTED",
                details=f"Agent output contained banned pesticide: '{pesticide}'",
                status="WARN"
            )
            # Redact/replace the banned pesticide name with a warning flag
            agent_response = agent_response.replace(
                pesticide.title(), f"[⚠️ BANNED SUBSTANCE BLOCKED: {pesticide.upper()}]"
            ).replace(
                pesticide, f"[⚠️ BANNED SUBSTANCE BLOCKED: {pesticide.upper()}]"
            )
            
    # 2. Check if chemical fungicides are mentioned and append disclaimer if not already there
    has_chemical = any(chem in lower_response for chem in CHEMICAL_FUNGICIDES)
    has_disclaimer = "chemical safety warning" in lower_response
    
    if has_chemical and not has_disclaimer:
        log_event(
            user=user,
            role=role,
            action="DISCLAIMER_APPENDED",
            details="Appended chemical safety disclaimer to agent recommendation.",
            status="SUCCESS"
        )
        agent_response += CHEMICAL_SAFETY_DISCLAIMER
        
    return agent_response
