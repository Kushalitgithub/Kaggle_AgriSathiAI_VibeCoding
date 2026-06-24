# AgriSathi AI 🌿
**Multi-Agent Agricultural Intelligence Platform**
*Kaggle AI Agents Intensive Vibe Coding Capstone Project • Track: Agents for Good*

---

AgriSathi AI is an award-winning production-quality AI agent system designed to support smallholder farmers in making critical decisions regarding crop pathology, weather risks, fertilizer application, farm planning, and market pricing.

---

## 📖 Table of Contents
1. [Problem Statement](#-problem-statement)
2. [Multi-Agent Architecture](#-multi-agent-architecture)
3. [Model Context Protocol (MCP) Integration](#-model-context-protocol-mcp-integration)
4. [Agent Skills](#-agent-skills)
5. [Security & Governance Features](#-security--governance-features)
6. [Antigravity Demonstration Workflow](#-antigravity-demonstration-workflow)
7. [Installation & Local Run Guide](#-installation--local-run-guide)
8. [Deployment Instructions](#-deployment-instructions)
9. [📹 5-Minute Video Pitch & Demo Outline](#-5-minute-video-pitch--demo-outline)

---

## 🚨 Problem Statement
Smallholder farmers globally face significant losses due to lack of timely, localized expertise. Issues include:
- Unidentified crop pests and diseases leading to crop failure.
- Inability to forecast localized weather risks (e.g. frost, fungal moisture conditions).
- Poor soil nutrition management and pesticide misuse.
- Volatile commodity pricing and lack of direct market insights.
- Language barriers translating technical guidelines.

AgriSathi AI addresses these challenges by coordinating a team of specialized ADK agents to deliver integrated, actionable advice in real time.

---

## 🤖 Multi-Agent Architecture
AgriSathi AI utilizes the **Google Agent Development Kit (ADK)** to orchestrate a team of seven specialized agents:

1. **Orchestrator Agent**: The central coordinator that plans agent participation, manages session memory, chains states, and aggregates reports.
2. **Crop Doctor Agent**: Inspects plant leaf imagery using multimodal Gemini Vision inputs to diagnose pathogens and compile remedies.
3. **Weather Intelligence Agent**: Communicates with the Weather MCP to assess localized environmental risks (e.g., humidity spikes matching disease spread models).
4. **Fertilizer Advisor Agent**: Analyzes crop health to build balanced N-P-K schedules and suggest organic, bio-friendly alternatives.
5. **Market Intelligence Agent**: Queries regional markets using the Market MCP to determine selling prices and crop storage opportunities.
6. **Farm Planner Agent**: Creates 4-week recovery calendars with milestone checkboxes.
7. **Nepali Language Agent**: Localizes final recommendations into a simple, polite, and voice-friendly Nepali translation.

---

## 🔌 Model Context Protocol (MCP) Integration
Exposes tools via 3 FastMCP servers to retrieve real-time data:
- **Weather Server**: Returns forecasts and processes parameters to detect high-risk boundaries (frost, blight growth conditions).
- **Market Server**: Connects to the SQLite database to supply pricing and historical seasonality curves.
- **Knowledge Server**: Searches pathology profiles and fetches treatment guides.

---

## 🛠️ Agent Skills
Reusable modular skills under `skills/`:
- **Diagnosis Skill**: Performs database lookups and multimodal classification.
- **Weather Analysis Skill**: Computes weather-driven crop alerts.
- **Market Forecasting Skill**: Runs sell-vs-hold seasonality predictions.
- **Planning Skill**: Formulates operational week-by-week farm schedules.
- **Summarization Skill**: Condenses multi-agent outputs into an executive dashboard card.
- **Translation Skill**: Localizes text into Nepalese dialect.
- **Report Generation Skill**: Compiles comprehensive reports.

---

## 🛡️ Security & Governance Features
Built to meet strict production-quality requirements:
1. **Passcode Authentication & RBAC**: Sidebar controls mapping passwords to roles:
   - **Farmer** (`1234`): Basic diagnostic scans, local prices, task checklists.
   - **Advisor** (`5678`): Access to compile advanced reports.
   - **Admin** (`9999`): Full control, access parameters, and security log grid.
2. **Prompt Injection Defense**: Filters inputs against jailbreak patterns (`ignore previous instructions`, `dan mode`, etc.). Blocked attempts are intercepted and logged as `BLOCKED`.
3. **Tool Permission Governance**: Prompts users in the UI to approve critical write-actions before execution.
4. **Input Validation**: Restricts attachments to image formats (PNG, JPG, JPEG, WEBP) and sizes below 5MB.
5. **Safe Response Filter**: Scans model responses for banned pesticides (e.g. Paraquat) and redacts them, adding chemical safety disclaimers automatically.
6. **Audit Trail**: Logs all events to an SQLite audit database.

---

## ⚡ Antigravity Demonstration Workflow
AgriSathi AI chains actions autonomously across the agents:
1. **Farmer uploads crop leaf image** ->
2. **Crop Doctor** diagnoses disease type (e.g. Tomato Late Blight) ->
3. **Weather Agent** checks humidity levels (e.g. 88% humidity flag) ->
4. **Fertilizer Agent** restricts nitrogen inputs to contain the fungus ->
5. **Market Agent** computes local average price and recommends a sell action ->
6. **Farm Planner** creates a 4-week task checklist ->
7. **Orchestrator** compiles the comprehensive directive ->
8. **Nepali Agent** localizes the summary ->
9. **Final report is rendered and made available for download**.

 <img width="1920" height="958" alt="Image" src="https://github.com/user-attachments/assets/bc87eb9e-1e7a-4dc6-b0e6-6967203dbb26" />

 <img width="1920" height="958" alt="Image" src="https://github.com/user-attachments/assets/5fadb30c-2649-4420-a9ff-3d46e9443784" />

---

## 💻 Installation & Local Run Guide

### Prerequisites
- Python 3.10+
- SQLite3

### Setup Steps
1. Clone the project files.
2. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```
4. Seed the database:
   ```bash
   python database/seed_db.py
   ```
5. Run the Streamlit Dashboard:
   ```bash
   streamlit run app.py
   ```

---

## 🚀 Deployment Instructions

### Google Cloud Run
1. Build the Docker container:
   ```bash
   gcloud builds submit --tag gcr.io/[PROJECT_ID]/agrisathi-ai
   ```
2. Deploy to Cloud Run:
   ```bash
   gcloud run deploy agrisathi-ai \
     --image gcr.io/[PROJECT_ID]/agrisathi-ai \
     --platform managed \
     --allow-unauthenticated \
     --port 8501
   ```

---

## 📹 5-Minute Video Pitch & Demo Outline

1. **Problem Statement (0:00 - 0:45)**: Show how crop failure, weather shifts, and market isolation devastate smallholder farmers. Introduce AgriSathi AI as an integrated companion.
2. **Why Agents & Architecture (0:45 - 1:30)**: Explain that static tools fail because farm issues are interconnected. Present the Google ADK 7-agent tree.
3. **MCP Demonstration (1:30 - 2:15)**: Show how the Weather, Market, and Knowledge MCP servers connect LLM agents to local datasets.
4. **Security Features (2:15 - 3:00)**: Highlight RBAC (Farmer, Advisor, Admin), prompt injection blocks, banned pesticide redaction, and database audit logs.
5. **Live Demo of Antigravity Workflow (3:00 - 4:15)**: Demonstrate uploading an image, the live Agent Activity Pipeline executing, and the final English/Nepali report generation.
6. **Deployment & Wrap Up (4:15 - 5:00)**: Show Cloud Run packaging and outline impact goals for smallholder farmers.
# Kaggle_AgriSathiAI_VibeCoding
