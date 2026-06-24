from mcp_servers.market_mcp import get_crop_price, analyze_market_trends

def forecast_market(crop: str, district: str = "Kathmandu") -> dict:
    """
    Retrieves current prices and historical trend forecasts for a crop.
    
    Returns:
        dict: {
            "current_prices": str,
            "trends": str,
            "crop": str
        }
    """
    prices_text = get_crop_price(crop, district)
    trends_text = analyze_market_trends(crop)
    
    return {
        "current_prices": prices_text,
        "trends": trends_text,
        "crop": crop
    }
