import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "agrisathi.db")

def create_and_seed():
    print(f"Creating database at {DB_PATH}...")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 1. Create Tables
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS crop_knowledge (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        crop TEXT NOT NULL,
        condition_name TEXT NOT NULL,
        type TEXT NOT NULL,
        symptoms TEXT,
        organic_treatment TEXT,
        chemical_treatment TEXT,
        preventative_measures TEXT,
        confidence_score REAL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS market_prices (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        crop TEXT NOT NULL,
        market TEXT NOT NULL,
        price_min REAL,
        price_max REAL,
        price_avg REAL,
        last_updated TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS market_trends (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        crop TEXT NOT NULL,
        month TEXT NOT NULL,
        avg_price REAL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS audit_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT NOT NULL,
        user TEXT NOT NULL,
        role TEXT NOT NULL,
        action TEXT NOT NULL,
        details TEXT,
        status TEXT NOT NULL
    )
    """)

    # 2. Seed Data
    # 2.1 Crop Knowledge
    knowledge_data = [
        # Tomato Late Blight
        (
            "Tomato",
            "Late Blight",
            "disease",
            "Dark, water-soaked spots on leaves that turn brown/black; white mold growth on the undersides under wet conditions; large dark lesions on stems and green/ripe fruits.",
            "Apply copper octanoate (copper soap) or organic Bordeaux mixture. Practice crop rotation (avoid planting with potatoes/peppers). Mulch the soil to prevent spore splash.",
            "Apply chemical fungicides such as Chlorothalonil, Mancozeb, or Metalaxyl-M. Spray immediately upon visual identification or when weather humidity exceeds 85%.",
            "Use certified disease-free seeds and disease-resistant cultivars (e.g., 'Defiant', 'Mountain Merit'). Space plants to optimize air circulation and water plants at the base.",
            0.88
        ),
        # Tomato Early Blight
        (
            "Tomato",
            "Early Blight",
            "disease",
            "Brown spots with concentric rings (target-like pattern) on older leaves first; leaves turn yellow and drop; dark leathery spots at the stem end of fruits.",
            "Apply Bacillus subtilis bio-fungicide or compost tea. Prune lower leaves to improve airflow and remove infected plant debris immediately.",
            "Spray with copper-based chemical fungicides or Chlorothalonil every 7-14 days during warm, humid weather.",
            "Rotate crops on a 3-year cycle. Ensure balanced soil nutrition with high calcium to build cell wall resistance. Water using drip irrigation to avoid wet leaves.",
            0.85
        ),
        # Rice Blast
        (
            "Rice",
            "Blast Disease",
            "disease",
            "Spindle-shaped lesions (diamond shaped) with reddish-brown borders and gray centers on leaves; neck rot causing stems to collapse and heads to lodge.",
            "Use bio-control agents like Trichoderma harzianum. Balance nitrogen levels (excessive nitrogen promotes blast growth). Destroy infected stubble after harvest.",
            "Apply systemic chemical fungicides such as Tricyclazole, Azoxystrobin, or Isoprothiolane at the leaf blast stage or early heading.",
            "Plant resistant rice varieties. Maintain stable water level in fields. Avoid late planting and excessive nitrogen fertilization.",
            0.92
        ),
        # Rice Stem Borer
        (
            "Rice",
            "Stem Borer",
            "pest",
            "Drying of the central tiller ('dead heart') during vegetative stage; white, empty panicles ('white head') during reproductive stage; tiny holes in stems.",
            "Release Trichogramma chilonis wasps (egg parasites). Set up light traps to capture adult moths. Harvest crops close to ground level to kill larvae in stems.",
            "Apply systemic insecticides like Cartap Hydrochloride or Chlorantraniliprole granules into standing water.",
            "Synchronize planting dates in the community. Remove weed hosts near canals. Apply balanced nitrogen fertilizer.",
            0.89
        ),
        # Potato Bacterial Wilt
        (
            "Potato",
            "Bacterial Wilt",
            "disease",
            "Rapid wilting of leaves, starting from top/branches during hot daytime; slimy brown discoloration of the vascular ring inside tubers when cut.",
            "Implement strict field sanitation. Solarize the soil. Plant companion crops like marigold. Avoid fields with a history of wilt for at least 5 years.",
            "No effective chemical cures exist for bacterial wilt. Use bactericides like Copper Oxychloride only to limit secondary spread.",
            "Always use certified disease-free seed tubers. Rotate fields with non-host crops like maize or wheat. Disinfect all farming tools.",
            0.82
        ),
        # Healthy Crop examples
        (
            "Tomato",
            "Healthy",
            "healthy",
            "Vibrant green leaves, uniform growth, sturdy stems, flowers, and fruits free of lesions, discoloration, spots, or abnormal wilting.",
            "Maintain general organic farming practices: compost application, compost tea foliar sprays, companion planting.",
            "No chemical fungicides or insecticides required. Apply preventative neem oil sprays periodically.",
            "Continue regular watering, monitoring, and weeding. Maintain soil health.",
            0.99
        ),
        (
            "Rice",
            "Healthy",
            "healthy",
            "Healthy green tillers, strong stems, uniform heading, erect leaves, clean golden panicles at maturity with no symptoms of lodging or decay.",
            "Maintain proper organic soil fertility and water levels.",
            "No chemical treatment necessary.",
            "Monitor field water levels regularly and weed during the early growth stages.",
            0.99
        )
    ]

    cursor.executemany("""
    INSERT INTO crop_knowledge (crop, condition_name, type, symptoms, organic_treatment, chemical_treatment, preventative_measures, confidence_score)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, knowledge_data)

    # 2.2 Market Prices (Nepalese markets)
    market_data = [
        ("Tomato", "Kalimati, Kathmandu", 65.0, 85.0, 75.0, "2026-06-24"),
        ("Tomato", "Birtamod, Jhapa", 55.0, 70.0, 62.5, "2026-06-24"),
        ("Tomato", "Pokhara, Kaski", 70.0, 90.0, 80.0, "2026-06-24"),
        ("Rice", "Kalimati, Kathmandu", 90.0, 110.0, 100.0, "2026-06-24"),
        ("Rice", "Birtamod, Jhapa", 75.0, 88.0, 81.5, "2026-06-24"),
        ("Rice", "Dharan, Sunsari", 80.0, 95.0, 87.5, "2026-06-24"),
        ("Potato", "Kalimati, Kathmandu", 40.0, 52.0, 46.0, "2026-06-24"),
        ("Potato", "Pokhara, Kaski", 45.0, 58.0, 51.5, "2026-06-24"),
        ("Maize", "Birtamod, Jhapa", 35.0, 45.0, 40.0, "2026-06-24"),
        ("Cardamom", "Birtamod, Jhapa", 1200.0, 1400.0, 1300.0, "2026-06-24")
    ]

    cursor.executemany("""
    INSERT INTO market_prices (crop, market, price_min, price_max, price_avg, last_updated)
    VALUES (?, ?, ?, ?, ?, ?)
    """, market_data)

    # 2.3 Market Trends (Historical Prices by Month)
    trend_data = [
        # Tomato
        ("Tomato", "Jan", 45.0), ("Tomato", "Feb", 50.0), ("Tomato", "Mar", 55.0),
        ("Tomato", "Apr", 65.0), ("Tomato", "May", 85.0), ("Tomato", "Jun", 75.0),
        ("Tomato", "Jul", 80.0), ("Tomato", "Aug", 95.0), ("Tomato", "Sep", 90.0),
        ("Tomato", "Oct", 70.0), ("Tomato", "Nov", 60.0), ("Tomato", "Dec", 50.0),
        # Rice
        ("Rice", "Jan", 80.0), ("Rice", "Feb", 80.0), ("Rice", "Mar", 82.0),
        ("Rice", "Apr", 85.0), ("Rice", "May", 85.0), ("Rice", "Jun", 90.0),
        ("Rice", "Jul", 95.0), ("Rice", "Aug", 100.0), ("Rice", "Sep", 98.0),
        ("Rice", "Oct", 92.0), ("Rice", "Nov", 85.0), ("Rice", "Dec", 80.0),
        # Potato
        ("Potato", "Jan", 30.0), ("Potato", "Feb", 32.0), ("Potato", "Mar", 35.0),
        ("Potato", "Apr", 40.0), ("Potato", "May", 45.0), ("Potato", "Jun", 46.0),
        ("Potato", "Jul", 48.0), ("Potato", "Aug", 55.0), ("Potato", "Sep", 58.0),
        ("Potato", "Oct", 52.0), ("Potato", "Nov", 42.0), ("Potato", "Dec", 35.0)
    ]

    cursor.executemany("""
    INSERT INTO market_trends (crop, month, avg_price)
    VALUES (?, ?, ?)
    """, trend_data)

    # 2.4 Audit Log seed
    cursor.execute("""
    INSERT INTO audit_logs (timestamp, user, role, action, details, status)
    VALUES (datetime('now'), 'system', 'Admin', 'DATABASE_SEED', 'Successfully created and seeded database with ag-knowledge and market trends.', 'SUCCESS')
    """)

    conn.commit()
    conn.close()
    print("Database seeding completed successfully.")

if __name__ == "__main__":
    create_and_seed()
