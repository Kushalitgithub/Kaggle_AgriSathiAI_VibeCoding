from fastmcp import FastMCP
import sqlite3
import os

mcp = FastMCP("Agricultural Knowledge Server")
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "database", "agrisathi.db")

@mcp.tool()
def search_disease_db(crop_name: str, disease_query: str) -> str:
    """
    Searches agricultural database for symptoms or disease profiles matching a query.
    Args:
        crop_name: Crop category (e.g. Tomato, Rice, Potato).
        disease_query: Text keywords relating to symptoms or condition names.
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        query = """
            SELECT condition_name, type, symptoms, confidence_score 
            FROM crop_knowledge 
            WHERE LOWER(crop) = LOWER(?) AND (LOWER(condition_name) LIKE LOWER(?) OR LOWER(symptoms) LIKE LOWER(?))
        """
        like_pattern = f"%{disease_query}%"
        cursor.execute(query, (crop_name, like_pattern, like_pattern))
        records = cursor.fetchall()
        conn.close()
        
        if not records:
            return f"No disease or symptom profiles matched your search '{disease_query}' for crop '{crop_name}'."
            
        report = f"### Agricultural Knowledge Match for {crop_name.title()} - '{disease_query}'\n"
        for rec in records:
            cond, cond_type, symptoms, conf = rec
            report += (
                f"- **Condition Name:** {cond} (Type: {cond_type.capitalize()})\n"
                f"  - **Symptoms:** {symptoms}\n"
                f"  - **Baseline Detection Confidence:** {conf * 100:.1f}%\n"
            )
        return report
    except Exception as e:
        return f"Error searching knowledge database: {e}"

@mcp.tool()
def get_treatment_plan(condition_name: str) -> str:
    """
    Retrieves full organic, chemical, and preventative treatment schedules for a specific crop condition.
    Args:
        condition_name: Name of the disease or pest condition (e.g., 'Late Blight', 'Blast Disease').
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT crop, condition_name, organic_treatment, chemical_treatment, preventative_measures 
            FROM crop_knowledge 
            WHERE LOWER(condition_name) = LOWER(?)
        """, (condition_name,))
        record = cursor.fetchone()
        conn.close()
        
        if not record:
            return f"No treatment plan found for condition: '{condition_name}'."
            
        crop, cond, organic, chemical, preventative = record
        
        plan = (
            f"### Comprehensive Treatment Plan for {crop} - **{cond}**\n\n"
            f"🌿 **Organic / Bio-rational Treatments:**\n"
            f"{organic}\n\n"
            f"🧪 **Chemical / Synthetic Controls:**\n"
            f"{chemical}\n\n"
            f"🛡️ **Long-term Preventative Measures:**\n"
            f"{preventative}"
        )
        return plan
    except Exception as e:
        return f"Error retrieving treatment plan: {e}"

if __name__ == "__main__":
    mcp.run()
