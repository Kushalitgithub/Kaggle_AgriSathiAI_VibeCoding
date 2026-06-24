# Setup and Deployment Guide

This guide provides step-by-step instructions to configure, test, and deploy **AgriSathi AI**.

---

## 1. Local Setup Instructions

### System Prerequisites
Ensure you have the following installed on your system:
- **Python 3.10 or higher**
- **SQLite3**
- **pip** and **virtualenv**

### Steps
1. **Navigate to the workspace**:
   ```bash
   cd /home/kushal/Desktop/Kaggle/Capston_Projrct
   ```
2. **Create a virtual environment**:
   ```bash
   python3 -m venv venv
   ```
3. **Activate the virtual environment**:
   ```bash
   source venv/bin/activate
   ```
4. **Install all required packages**:
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```
5. **Seed the Agricultural & Market Database**:
   ```bash
   python database/seed_db.py
   ```
6. **Set up environment variables**:
   Create a `.env` file in the root directory:
   ```env
   GEMINI_API_KEY=your_gemini_api_key_here
   ```
7. **Run the Streamlit Web Application**:
   ```bash
   streamlit run app.py
   ```
   Open your browser to `http://localhost:8501`.

---

## 2. Running and Testing the MCP Servers

You can run individual MCP servers directly in python or test them using the `fastmcp` CLI:

### Standard Execution
```bash
python mcp_servers/weather_mcp.py
python mcp_servers/market_mcp.py
python mcp_servers/knowledge_mcp.py
```

### testing with FastMCP CLI
```bash
fastmcp run mcp_servers/weather_mcp.py
fastmcp run mcp_servers/market_mcp.py
fastmcp run mcp_servers/knowledge_mcp.py
```

---

## 3. Running Unit Tests
Validate all security, role access, and database systems before deployment:
```bash
python -m unittest tests/test_agents.py
```

---

## 4. Container Deployment (Docker)

### Building the Image Locally
```bash
docker build -t agrisathi-ai:latest .
```

### Running the Container Locally
```bash
docker run -p 8501:8501 --env GEMINI_API_KEY="your_api_key" agrisathi-ai:latest
```

---

## 5. Google Cloud Run Deployment

1. **Enable required Google Cloud APIs**:
   ```bash
   gcloud services enable run.googleapis.com containerregistry.googleapis.com builds.googleapis.com
   ```
2. **Build and push your image to Google Container Registry**:
   ```bash
   gcloud builds submit --tag gcr.io/[YOUR_GCP_PROJECT_ID]/agrisathi-ai
   ```
3. **Deploy to Cloud Run**:
   ```bash
   gcloud run deploy agrisathi-ai \
     --image gcr.io/[YOUR_GCP_PROJECT_ID]/agrisathi-ai \
     --platform managed \
     --allow-unauthenticated \
     --port 8501 \
     --set-env-vars GEMINI_API_KEY="your_api_key"
   ```
4. Copy the secure HTTPS service link provided in the command line and share it as the active platform URL!
