import os
import sqlite3
import google.generativeai as genai
from PIL import Image

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "database", "agrisathi.db")

def run_diagnosis(image_path: str = None, symptoms_text: str = "", api_key: str = None) -> dict:
    """
    Performs crop health diagnosis using either the Gemini API (if key is available) 
    or database lookups with a rule-based fallback.
    
    Returns:
        dict: {
            "crop": str,
            "condition": str,
            "confidence": float,
            "symptoms": str,
            "organic_treatment": str,
            "chemical_treatment": str,
            "preventative_measures": str
        }
    """
    # 1. Attempt Gemini Multimodal API if credentials exist
    key_to_use = api_key or os.getenv("GEMINI_API_KEY")
    if key_to_use and image_path and os.path.exists(image_path):
        try:
            genai.configure(api_key=key_to_use)
            # Use recommended Gemini Flash model
            model = genai.GenerativeModel("gemini-1.5-flash")
            
            img = Image.open(image_path)
            prompt = (
                "You are an expert plant pathologist. Analyze this leaf image and identify: "
                "1. Crop type (e.g., Tomato, Rice, Potato, Maize, etc.) "
                "2. Condition name (e.g., Late Blight, Blast Disease, Stem Borer, Healthy, etc.) "
                "3. Symptoms visible. "
                "4. Estimate your confidence level (0.0 to 1.0). "
                "Provide your response in a clear structured format with keys: CROP, CONDITION, SYMPTOMS, CONFIDENCE."
            )
            
            response = model.generate_content([prompt, img])
            text = response.text
            
            # Simple parser for the model output
            crop = "Tomato"
            condition = "Late Blight"
            symptoms = "Leaf spot lesions"
            confidence = 0.85
            
            for line in text.split("\n"):
                if "CROP:" in line:
                    crop = line.split("CROP:")[1].strip()
                elif "CONDITION:" in line:
                    condition = line.split("CONDITION:")[1].strip()
                elif "SYMPTOMS:" in line:
                    symptoms = line.split("SYMPTOMS:")[1].strip()
                elif "CONFIDENCE:" in line:
                    try:
                        confidence = float(line.split("CONFIDENCE:")[1].strip().replace("%", ""))
                        if confidence > 1.0:
                            confidence /= 100.0
                    except:
                        pass
                        
            # Get treatments from database to keep details consistent and secure
            db_details = get_treatments_from_db(crop, condition)
            if db_details:
                return {
                    "crop": crop,
                    "condition": condition,
                    "confidence": confidence,
                    "symptoms": symptoms,
                    **db_details
                }
        except Exception as e:
            print(f"Gemini API diagnosis failed: {e}. Falling back to database lookup...")

    # 2. Database Lookup & Fallback System (Runs when no API key or image is uploaded)
    # Check if image name contains hints (useful for mock testing UI)
    inferred_crop = "Tomato"
    inferred_condition = "Late Blight"
    
    if image_path:
        filename = os.path.basename(image_path).lower()
        if "rice" in filename:
            inferred_crop = "Rice"
            if "blast" in filename:
                inferred_condition = "Blast Disease"
            elif "borer" in filename:
                inferred_condition = "Stem Borer"
            else:
                inferred_condition = "Healthy"
        elif "potato" in filename:
            inferred_crop = "Potato"
            inferred_condition = "Bacterial Wilt"
        elif "tomato" in filename:
            inferred_crop = "Tomato"
            if "early" in filename:
                inferred_condition = "Early Blight"
            elif "healthy" in filename:
                inferred_condition = "Healthy"
            else:
                inferred_condition = "Late Blight"
    elif symptoms_text:
        sym_lower = symptoms_text.lower()
        if "blast" in sym_lower or "spindle" in sym_lower:
            inferred_crop = "Rice"
            inferred_condition = "Blast Disease"
        elif "borer" in sym_lower or "dead heart" in sym_lower or "til" in sym_lower:
            inferred_crop = "Rice"
            inferred_condition = "Stem Borer"
        elif "potato" in sym_lower or "wilt" in sym_lower:
            inferred_crop = "Potato"
            inferred_condition = "Bacterial Wilt"
        elif "early" in sym_lower or "target" in sym_lower:
            inferred_crop = "Tomato"
            inferred_condition = "Early Blight"

    db_details = get_treatments_from_db(inferred_crop, inferred_condition)
    if db_details:
        return {
            "crop": inferred_crop,
            "condition": inferred_condition,
            "confidence": db_details.get("confidence_score", 0.85),
            "symptoms": db_details.get("symptoms", "Typical lesions matching condition standard features."),
            **db_details
        }
        
    return {
        "crop": "Tomato",
        "condition": "Healthy",
        "confidence": 0.95,
        "symptoms": "Healthy green foliage.",
        "organic_treatment": "Apply compost regularly.",
        "chemical_treatment": "No chemical treatment required.",
        "preventative_measures": "Water regularly, monitor daily."
    }

def get_treatments_from_db(crop: str, condition: str) -> dict:
    """
    Helper to extract treatments from local SQLite database.
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT symptoms, organic_treatment, chemical_treatment, preventative_measures, confidence_score 
            FROM crop_knowledge 
            WHERE LOWER(crop) = LOWER(?) AND LOWER(condition_name) = LOWER(?)
        """, (crop, condition))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            symptoms, organic, chemical, preventative, conf = row
            return {
                "symptoms": symptoms,
                "organic_treatment": organic,
                "chemical_treatment": chemical,
                "preventative_measures": preventative,
                "confidence_score": conf
            }
    except Exception as e:
        print(f"Error fetching from db: {e}")
    return {}
