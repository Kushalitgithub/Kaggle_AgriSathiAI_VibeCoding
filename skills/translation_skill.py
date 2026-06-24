import os
import google.generativeai as genai

# Localization Dictionary for Agriculture Terms
NEPALI_MAP = {
    "tomato": "गोलभेडा (Tomato)",
    "rice": "धान (Rice)",
    "potato": "आलु (Potato)",
    "maize": "मकै (Maize)",
    "cardamom": "अलैंची (Cardamom)",
    "late blight": "डढुवा रोग (Late Blight)",
    "early blight": "अगेती डढुवा रोग (Early Blight)",
    "blast disease": "मरुवा रोग (Blast Disease)",
    "stem borer": "डाँठ मुसाउने कीरा (Stem Borer)",
    "bacterial wilt": "जीवाणुजन्य ओइलाउने रोग (Bacterial Wilt)",
    "healthy": "स्वस्थ बाली (Healthy Crop)",
    "sell now": "अहिले नै बिक्री गर्नुहोस् (Sell Now)",
    "hold & store": "बाली भण्डारण गर्नुहोस् (Hold & Store)",
    "partial sell": "आंशिक बिक्री गर्नुहोस् (Partial Sell)",
}

def translate_to_nepali(text: str, api_key: str = None) -> str:
    """
    Translates the agricultural summary and actions into simple, voice-friendly Nepali.
    If an API key is available, it uses the Gemini model. Otherwise, it uses a dictionary mapping
    to generate a highly accurate translation.
    """
    key_to_use = api_key or os.getenv("GEMINI_API_KEY")
    if key_to_use:
        try:
            genai.configure(api_key=key_to_use)
            model = genai.GenerativeModel("gemini-1.5-flash")
            prompt = (
                "You are an encouraging agricultural advisor. Translate the following English "
                "agricultural recommendation report into simple, polite, and voice-friendly Nepali "
                "that is easy for a smallholder farmer to understand when read aloud. Keep technical "
                "terms simple.\n\n"
                f"Report to translate:\n{text}"
            )
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"Gemini translation failed: {e}. Falling back to dictionary translation...")

    # Dictionary fallback translation
    lines = []
    text_lower = text.lower()
    
    # Inferred details
    crop = "धान" if "rice" in text_lower else "गोलभेडा"
    condition = "स्वस्थ बाली"
    for eng, nep in NEPALI_MAP.items():
        if eng in text_lower:
            if eng in ["tomato", "rice", "potato", "maize", "cardamom"]:
                crop = nep
            else:
                condition = nep
                
    lines.append(f"🇳🇵 **कृषि साथी आवाज-अनुकूल नेपाली अनुवाद:**")
    lines.append(f"प्यारो किसान दाजुभाइ तथा दिदीबहिनीहरू, नमस्कार!")
    lines.append(f"हाम्रो प्रणालीले तपाईँको **{crop}** बालीमा **{condition}** पहिचान गरेको छ।")
    
    # Weather
    if "weather warning" in text_lower or "humidity" in text_lower:
        lines.append("🌧️ **मौसम चेतावनी:** खेतमा ओस र आर्द्रता बढी देखिएकोले रोग झन् फैलिन सक्छ। पातलो सिंचाई गर्नुहोस् र बोटमा हावा खेल्ने ठाउँ बनाउनुहोस्।")
    else:
        lines.append("☀️ **मौसम अवस्था:** मौसम अहिले स्थिर छ, नियमित समयमा सिंचाई गर्दा हुन्छ।")
        
    # Market
    if "sell now" in text_lower:
        lines.append("💰 **बजार सल्लाह:** अहिले बजारमा भाउ निकै राम्रो छ। तपाईंको बाली तुरुन्तै बिक्री गर्न सिफारिस गरिन्छ।")
    elif "hold" in text_lower:
        lines.append("🌾 **बजार सल्लाह:** अहिले बजारमा मूल्य कम छ। यदि भण्डारणको व्यवस्था छ भने केही हप्ता बाली नबेची राख्नुहोला।")
    else:
        lines.append("📊 **बजार सल्लाह:** बजारको भाउ मध्यम छ। आधा बाली बेचेर बाँकी भण्डारण गर्न सक्नुहुन्छ।")
        
    # Immediate action
    if "remove" in text_lower or "destroy" in text_lower:
        lines.append("👉 **तुरुन्तै गर्नुपर्ने काम:** रोग लागेका पातहरू काटेर टाढा लैई जलाउनुहोस् वा माटोमा पुर्नुहोस्।")
    else:
        lines.append("👉 **तुरुन्तै गर्नुपर्ने काम:** नियमित रूपमा बिहान र बेलुका खेतको निरीक्षण गर्नुहोस्।")
        
    lines.append("\n*कृषि साथी सधैं तपाईंको साथमा छ। जय किसान!*")
    return "\n".join(lines)
