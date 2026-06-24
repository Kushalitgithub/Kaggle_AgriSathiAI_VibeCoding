from fastmcp import FastMCP
import sqlite3
import os

mcp = FastMCP("Market Intelligence Server")
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "database", "agrisathi.db")

@mcp.tool()
def get_crop_price(crop_name: str, market_name: str = "") -> str:
    """
    Retrieves current prices for a specific crop across markets.
    Args:
        crop_name: The name of the crop (e.g. Tomato, Rice, Potato).
        market_name: Optional market filter (e.g., 'Kalimati, Kathmandu').
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        query = "SELECT crop, market, price_min, price_max, price_avg, last_updated FROM market_prices WHERE LOWER(crop) = LOWER(?)"
        params = [crop_name]
        
        if market_name:
            query += " AND LOWER(market) LIKE LOWER(?)"
            params.append(f"%{market_name}%")
            
        cursor.execute(query, params)
        records = cursor.fetchall()
        conn.close()
        
        if not records:
            return f"No current price records found for crop: '{crop_name}' in market '{market_name or 'any'}'."
            
        report = f"### Current Market Prices for {crop_name.title()}\n"
        for rec in records:
            crop, market, p_min, p_max, p_avg, last_up = rec
            report += (
                f"- **Market:** {market}\n"
                f"  - Minimum Price: NPR {p_min}/kg\n"
                f"  - Maximum Price: NPR {p_max}/kg\n"
                f"  - Average Price: NPR {p_avg}/kg\n"
                f"  - Last Updated: {last_up}\n"
            )
        return report
    except Exception as e:
        return f"Error accessing market prices: {e}"

@mcp.tool()
def analyze_market_trends(crop_name: str) -> str:
    """
    Fetches historical monthly averages for a crop and performs a sell-vs-hold profitability analysis.
    Args:
        crop_name: Crop name to analyze.
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT month, avg_price FROM market_trends 
            WHERE LOWER(crop) = LOWER(?)
            ORDER BY CASE month 
                WHEN 'Jan' THEN 1 WHEN 'Feb' THEN 2 WHEN 'Mar' THEN 3 
                WHEN 'Apr' THEN 4 WHEN 'May' THEN 5 WHEN 'Jun' THEN 6 
                WHEN 'Jul' THEN 7 WHEN 'Aug' THEN 8 WHEN 'Sep' THEN 9 
                WHEN 'Oct' THEN 10 WHEN 'Nov' THEN 11 WHEN 'Dec' THEN 12 
            END
        """, (crop_name,))
        records = cursor.fetchall()
        
        # Get current avg price from market_prices
        cursor.execute("SELECT AVG(price_avg) FROM market_prices WHERE LOWER(crop) = LOWER(?)", (crop_name,))
        current_avg = cursor.fetchone()[0]
        conn.close()
        
        if not records:
            return f"No historical trend records found for crop: '{crop_name}'."
            
        trend_summary = f"### 12-Month Price Trend for {crop_name.title()}\n"
        months = []
        prices = []
        for month, price in records:
            months.append(month)
            prices.append(price)
            trend_summary += f"- {month}: NPR {price}/kg\n"
            
        if current_avg:
            trend_summary += f"\n- **Current Combined Market Avg:** NPR {current_avg:.2f}/kg\n"
            
            # Simple decision logic
            max_hist = max(prices)
            min_hist = min(prices)
            
            if current_avg >= max_hist * 0.9:
                decision = "🟢 **SELL NOW (Optimal opportunity)**"
                rationale = f"Current prices are close to the historical peak (NPR {max_hist}/kg). Demand is strong and supply is likely tight."
            elif current_avg <= min_hist * 1.1:
                decision = "🔴 **HOLD & STORE (Low market opportunity)**"
                rationale = f"Current prices are near historical lows (NPR {min_hist}/kg). If storage facilities are available, hold crops for 4-8 weeks when supply declines and prices adjust."
            else:
                decision = "🟡 **PARTIAL SELL (Moderate opportunity)**"
                rationale = "Prices are in the mid-range. Suggest selling 50% of the yield to cover immediate operational costs and storing the remainder for future price increases."
                
            trend_summary += f"\n**Market Opportunity Action Directive:**\n- **Recommendation:** {decision}\n- **Analysis:** {rationale}"
            
        return trend_summary
    except Exception as e:
        return f"Error retrieving market trends: {e}"

if __name__ == "__main__":
    mcp.run()
