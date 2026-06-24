import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Key configurations
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")

# Directory configurations
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_DIR = os.path.join(BASE_DIR, "database")
MCP_SERVERS_DIR = os.path.join(BASE_DIR, "mcp_servers")
AGENTS_DIR = os.path.join(BASE_DIR, "agents")
SKILLS_DIR = os.path.join(BASE_DIR, "skills")
SECURITY_DIR = os.path.join(BASE_DIR, "security")

# Ensure subdirectories exist
for path in [DATABASE_DIR, MCP_SERVERS_DIR, AGENTS_DIR, SKILLS_DIR, SECURITY_DIR]:
    os.makedirs(path, exist_ok=True)
