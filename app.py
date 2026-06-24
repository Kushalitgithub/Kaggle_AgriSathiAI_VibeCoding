import streamlit as st
import os
import time
import sqlite3
import pandas as pd
import plotly.express as px
from PIL import Image

# Import custom security layers
from security.auth import authenticate_user, has_permission
from security.input_sanitizer import check_prompt_injection, validate_image_upload
from security.output_filter import filter_agent_output
from security.tool_security import verify_tool_execution
from security.audit_logger import log_event, get_audit_logs

# Import ADK Orchestration
from agents.orchestrator import Orchestrator

# Page Configuration
st.set_page_config(
    page_title="AgriSathi AI - Agricultural Intelligence",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Premium Design & Rich Aesthetics
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&family=Inter:wght@300;400;500;600&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    .main-title {
        font-family: 'Outfit', sans-serif;
        font-weight: 700;
        background: linear-gradient(90deg, #11998e 0%, #38ef7d 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.8rem;
        margin-bottom: 0.2rem;
    }
    
    .sub-title {
        font-family: 'Outfit', sans-serif;
        color: #718096;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
    
    /* Card design with glassmorphism */
    .metric-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
        backdrop-filter: blur(5px);
        -webkit-backdrop-filter: blur(5px);
        margin-bottom: 1rem;
    }
    
    .metric-title {
        font-size: 0.9rem;
        color: #a0aec0;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 0.5rem;
    }
    
    .metric-value {
        font-size: 1.8rem;
        font-weight: 600;
        color: #38ef7d;
        font-family: 'Outfit', sans-serif;
    }
    
    /* Status Badge styling */
    .status-badge {
        padding: 0.25rem 0.6rem;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 600;
        display: inline-block;
    }
    
    .status-success {
        background-color: rgba(72, 187, 120, 0.15);
        color: #48bb78;
        border: 1px solid rgba(72, 187, 120, 0.3);
    }
    
    .status-blocked {
        background-color: rgba(245, 101, 101, 0.15);
        color: #f56565;
        border: 1px solid rgba(245, 101, 101, 0.3);
    }
    
    .status-warn {
        background-color: rgba(237, 137, 54, 0.15);
        color: #ed8936;
        border: 1px solid rgba(237, 137, 54, 0.3);
    }

    /* Agent Activity Pipeline indicators */
    .agent-pipeline-node {
        display: flex;
        align-items: center;
        margin-bottom: 0.8rem;
        padding: 0.6rem 1rem;
        border-radius: 8px;
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.05);
    }
    
    .agent-active {
        border-left: 4px solid #38ef7d;
        background: rgba(56, 239, 125, 0.05);
        animation: pulse 1.5s infinite alternate;
    }
    
    .agent-complete {
        border-left: 4px solid #4299e1;
        background: rgba(66, 153, 225, 0.05);
    }
    
    @keyframes pulse {
        0% { opacity: 0.7; }
        100% { opacity: 1; }
    }
</style>
""", unsafe_allow_html=True)

# Initialize Session States
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.role = "Guest"
    st.session_state.role_desc = ""
    st.session_state.user_id = "guest"
if "gemini_key" not in st.session_state:
    st.session_state.gemini_key = ""
if "orchestrator" not in st.session_state:
    st.session_state.orchestrator = None
if "agent_history" not in st.session_state:
    st.session_state.agent_history = []
if "consent_granted" not in st.session_state:
    st.session_state.consent_granted = False

# Database path for direct price/audit logs mapping
DB_PATH = os.path.join(os.path.dirname(__file__), "database", "agrisathi.db")

# --- SIDEBAR: Authentication & Key Management ---
with st.sidebar:
    st.image("https://img.icons8.com/color/96/sprout.png", width=64)
    st.markdown("<h2 style='font-family:Outfit; margin-top:0;'>AgriSathi AI</h2>", unsafe_allow_html=True)
    st.markdown("🧑‍🌾 *Your Multi-Agent Farming Companion*")
    st.markdown("---")
    
    # 1. Authentication
    st.markdown("### 🔐 Security & Access")
    if not st.session_state.authenticated:
        role_select = st.selectbox("Select Access Role", ["Farmer", "Advisor", "Admin"])
        passcode = st.text_input("Enter Passcode", type="password")
        if st.button("Authenticate"):
            success, role, desc = authenticate_user(passcode)
            if success:
                st.session_state.authenticated = True
                st.session_state.role = role
                st.session_state.role_desc = desc
                st.session_state.user_id = f"user_{role.lower()}"
                
                # Instantiate Orchestrator with the input key if available
                st.session_state.orchestrator = Orchestrator(api_key=st.session_state.gemini_key)
                st.success(f"Authenticated as {role}!")
                st.rerun()
            else:
                st.error(desc)
    else:
        st.markdown(f"**Current Role:** `{st.session_state.role}`")
        st.caption(st.session_state.role_desc)
        
        # Security Governance: Tool Write Consent checkbox
        st.session_state.consent_granted = st.checkbox("Grant Write Permissions to Agents", value=st.session_state.consent_granted)
        st.caption("Required for agents to generate calendar tasks and save reports.")
        
        if st.button("Logout"):
            st.session_state.authenticated = False
            st.session_state.role = "Guest"
            st.session_state.user_id = "guest"
            st.session_state.orchestrator = None
            st.session_state.consent_granted = False
            st.rerun()
            
    st.markdown("---")
    
    # 2. API Key Management
    st.markdown("### ⚙️ Engine Settings")
    input_key = st.text_input("Gemini API Key (Optional)", type="password", value=st.session_state.gemini_key)
    if input_key != st.session_state.gemini_key:
        st.session_state.gemini_key = input_key
        if st.session_state.orchestrator:
            st.session_state.orchestrator = Orchestrator(api_key=input_key)
        st.info("API Key updated. Engine reloaded.")
        
    st.caption("If empty, the platform will utilize localized database mappings and mock diagnostics for testing.")

# --- MAIN APP LAYOUT ---
st.markdown("<h1 class='main-title'>AgriSathi AI Platform</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-title'>Agents for Good track • Advanced Agricultural Decision Engine</p>", unsafe_allow_html=True)

if not st.session_state.authenticated:
    st.warning("🔒 Access Denied. Please input your passcode in the sidebar to select your role (e.g. Farmer: 1234, Advisor: 5678, Admin: 9999).")
    
    # Quick demo details
    st.info("""
    **Capstone Project Quick-Access Roles:**
    - **Farmer Passcode:** `1234` (Access to basic diagnostics, local market prices, calendar checklists)
    - **Advisor Passcode:** `5678` (Access to all farmer views + advanced reports compiling)
    - **Admin Passcode:** `9999` (Access to global parameters + real-time security audit log database)
    """)
else:
    # 4 tabs
    tabs = ["🏡 Dashboard", "🔬 Crop Doctor (Vision)", "📈 Market Forecasting", "📅 Farm Calendar", "🛡️ Security & Audit"]
    t_dash, t_doc, t_market, t_calendar, t_security = st.tabs(tabs)
    
    # Initialize orchestrator if somehow not set
    if not st.session_state.orchestrator:
        st.session_state.orchestrator = Orchestrator(api_key=st.session_state.gemini_key)
        
    # --- TAB 1: DASHBOARD ---
    with t_dash:
        st.markdown("### Farm Overview")
        
        # Metric Cards Layout
        m_col1, m_col2, m_col3 = st.columns(3)
        with m_col1:
            st.markdown("""
            <div class='metric-card'>
                <div class='metric-title'>Environmental Alert</div>
                <div class='metric-value' style='color:#f56565;'>⚠️ High Blight Risk</div>
                <p style='color:#a0aec0; margin-bottom:0; font-size:0.85rem;'>Humidity: 88% • Temp: 22°C</p>
            </div>
            """, unsafe_allow_html=True)
        with m_col2:
            st.markdown("""
            <div class='metric-card'>
                <div class='metric-title'>Market Opportunity</div>
                <div class='metric-value'>Tomato Peak</div>
                <p style='color:#a0aec0; margin-bottom:0; font-size:0.85rem;'>NPR 75.0/kg avg • Trend: +12%</p>
            </div>
            """, unsafe_allow_html=True)
        with m_col3:
            st.markdown("""
            <div class='metric-card'>
                <div class='metric-title'>Security Status</div>
                <div class='metric-value' style='color:#48bb78;'>🛡️ Active Guard</div>
                <p style='color:#a0aec0; margin-bottom:0; font-size:0.85rem;'>Prompt Defender: On • RBAC: Active</p>
            </div>
            """, unsafe_allow_html=True)
            
        # Chatbot Interface communicating with Orchestrator
        st.markdown("#### Ask AgriSathi Assistant")
        
        chat_container = st.container(height=300)
        with chat_container:
            for msg in st.session_state.agent_history:
                st.chat_message(msg["role"]).write(msg["content"])
                
        user_prompt = st.chat_input("Ask about weather risks, fertilizer schedules, or crop prices...")
        if user_prompt:
            # 1. Input Sanitization & Prompt Injection Defense
            is_safe, clean_prompt = check_prompt_injection(user_prompt, st.session_state.user_id, st.session_state.role)
            
            chat_container.chat_message("user").write(user_prompt)
            st.session_state.agent_history.append({"role": "user", "content": user_prompt})
            
            if not is_safe:
                chat_container.chat_message("assistant").error(clean_prompt)
                st.session_state.agent_history.append({"role": "assistant", "content": clean_prompt})
            else:
                with st.spinner("Orchestrator thinking..."):
                    # Process basic chat response (or execute agent)
                    # For simplicity, search database or general response
                    if "price" in clean_prompt.lower() or "market" in clean_prompt.lower():
                        # Call Market Agent
                        crop = "Tomato"
                        for c in ["Tomato", "Rice", "Potato", "Maize", "Cardamom"]:
                            if c.lower() in clean_prompt.lower():
                                crop = c
                        ans = st.session_state.orchestrator.market_agent.run(crop, "Kathmandu")
                        response_text = ans.get("current_prices") + "\n\n" + ans.get("trends")
                    elif "weather" in clean_prompt.lower() or "rain" in clean_prompt.lower() or "forecast" in clean_prompt.lower():
                        ans = st.session_state.orchestrator.weather_agent.run("Kathmandu")
                        response_text = ans.get("forecast") + "\n\n" + ans.get("risk_report")
                    elif "fertilizer" in clean_prompt.lower() or "nitrogen" in clean_prompt.lower():
                        ans = st.session_state.orchestrator.fertilizer_agent.run("Tomato", "Late Blight")
                        response_text = f"**Deficiency:** {ans['deficiency_warning']}\n\n**Schedule:** {ans['schedule']}\n\n**Alternatives:** {ans['organic_alternatives']}"
                    else:
                        response_text = (
                            "Hello! I am the AgriSathi Orchestrator. I coordinate multiple specialist agents "
                            "to answer your crop, weather, fertilizer, and market questions. "
                            "Please head to the **Crop Doctor (Vision)** tab to upload an image of a crop leaf and "
                            "trigger the autonomous Antigravity multi-agent workflow!"
                        )
                        
                    # Output Safe Filter
                    response_text = filter_agent_output(response_text, st.session_state.user_id, st.session_state.role)
                    
                    chat_container.chat_message("assistant").write(response_text)
                    st.session_state.agent_history.append({"role": "assistant", "content": response_text})

    # --- TAB 2: CROP DOCTOR & ANTIGRAVITY WORKFLOW ---
    with t_doc:
        st.markdown("### Crop Doctor Diagnostics & Autonomous Agent Chain")
        st.caption("Upload a leaf image of a diseased crop (e.g. Tomato Leaf with spots, Rice leaves, Potato leaf) to execute the end-to-end autonomous decision chain.")
        
        # File uploader
        uploaded_image = st.file_uploader("Upload Crop Leaf Image", type=["png", "jpg", "jpeg", "webp"])
        
        # Symptoms text input
        symptoms_text = st.text_input("Describe visible symptoms (optional, e.g. brown spots, yellow halo, dry leaves)", value="")
        
        # Display sample seed images selector if they don't have an image
        st.markdown("💡 *No image? Choose one of our pre-seeded diagnostic cases below:*")
        c_col1, c_col2, c_col3 = st.columns(3)
        sample_img_case = None
        with c_col1:
            if st.button("Sample 1: Tomato Late Blight"):
                sample_img_case = "tomato_late_blight.jpg"
        with c_col2:
            if st.button("Sample 2: Rice Blast"):
                sample_img_case = "rice_blast.jpg"
        with c_col3:
            if st.button("Sample 3: Potato Wilt"):
                sample_img_case = "potato_bacterial_wilt.jpg"
                
        # Validate Uploaded Image
        valid_upload = False
        active_image_path = None
        
        if uploaded_image:
            # Run image validation
            is_valid, msg = validate_image_upload(uploaded_image.name, uploaded_image.size, st.session_state.user_id, st.session_state.role)
            if is_valid:
                # Save file locally inside workspace
                os.makedirs("tmp", exist_ok=True)
                active_image_path = os.path.join("tmp", uploaded_image.name)
                with open(active_image_path, "wb") as f:
                    f.write(uploaded_image.getbuffer())
                valid_upload = True
                st.image(Image.open(active_image_path), width=250, caption="Uploaded leaf image")
            else:
                st.error(msg)
        elif sample_img_case:
            os.makedirs("tmp", exist_ok=True)
            active_image_path = os.path.join("tmp", sample_img_case)
            # Create a simple dummy empty file representing the sample image for mock triggers
            with open(active_image_path, "w") as f:
                f.write("sample image mock data")
            valid_upload = True
            st.success(f"Selected pre-seeded case: `{sample_img_case}`")

        # Execute Antigravity Workflow
        if valid_upload:
            location_inp = st.text_input("Farming Location / District", value="Kathmandu")
            
            # Tool permission management check for write-actions in workflow
            st.markdown("#### Tool Permission Authorization")
            if not st.session_state.consent_granted:
                st.warning("⚠️ Access Pending: Agents require write permission consent (check sidebar box) to update the calendar database and compile files.")
            
            if st.button("⚡ Run Autonomous Multi-Agent Chain"):
                # Run security check on tool execution
                allowed, err_msg = verify_tool_execution(
                    "write_farm_plan_schedule", 
                    st.session_state.user_id, 
                    st.session_state.role, 
                    required_role="Farmer", 
                    user_consent_given=st.session_state.consent_granted
                )
                
                if not allowed:
                    st.error(err_msg)
                else:
                    # Visual Pipeline Execution Indicators (Micro-animations)
                    st.markdown("#### Multi-Agent Activity Pipeline")
                    
                    p_nodes = [
                        ("orchestrator", "Orchestrator Agent: Initializing chain and mapping workflow..."),
                        ("crop_doctor", "Crop Doctor Agent: Analyzing leaf pathology..."),
                        ("weather", "Weather Agent: Fetching meteorological forecasts & risks..."),
                        ("fertilizer", "Fertilizer Advisor Agent: Formulating soil/NPK remedies..."),
                        ("market", "Market Agent: Retrieving commodity pricing and opportunity projections..."),
                        ("planner", "Farm Planner Agent: Compiling calendar recovery tasks..."),
                        ("translator", "Nepali Agent: Translating agricultural summaries to Nepali..."),
                        ("orchestrator_compile", "Orchestrator Agent: Finalizing farm directive report...")
                    ]
                    
                    # Create streamlit placeholders for activity updates
                    placeholders = {}
                    for key, text in p_nodes:
                        placeholders[key] = st.empty()
                        placeholders[key].markdown(f"<div class='agent-pipeline-node'>⚪ {text}</div>", unsafe_allow_html=True)
                        
                    # Simulate step-by-step executions
                    # Step 1: Orchestrator Start
                    placeholders["orchestrator"].markdown(f"<div class='agent-pipeline-node agent-active'>⏳ Orchestrator Agent: Initializing chain and mapping workflow...</div>", unsafe_allow_html=True)
                    time.sleep(0.6)
                    placeholders["orchestrator"].markdown(f"<div class='agent-pipeline-node agent-complete'>✓ Orchestrator Agent: Initializing chain and mapping workflow...</div>", unsafe_allow_html=True)
                    
                    # Step 2: Crop Doctor
                    placeholders["crop_doctor"].markdown(f"<div class='agent-pipeline-node agent-active'>⏳ Crop Doctor Agent: Analyzing leaf pathology...</div>", unsafe_allow_html=True)
                    time.sleep(1.0)
                    placeholders["crop_doctor"].markdown(f"<div class='agent-pipeline-node agent-complete'>✓ Crop Doctor Agent: Analyzing leaf pathology...</div>", unsafe_allow_html=True)
                    
                    # Step 3: Weather
                    placeholders["weather"].markdown(f"<div class='agent-pipeline-node agent-active'>⏳ Weather Agent: Fetching meteorological forecasts & risks...</div>", unsafe_allow_html=True)
                    time.sleep(0.8)
                    placeholders["weather"].markdown(f"<div class='agent-pipeline-node agent-complete'>✓ Weather Agent: Fetching meteorological forecasts & risks...</div>", unsafe_allow_html=True)
                    
                    # Step 4: Fertilizer
                    placeholders["fertilizer"].markdown(f"<div class='agent-pipeline-node agent-active'>⏳ Fertilizer Advisor Agent: Formulating soil/NPK remedies...</div>", unsafe_allow_html=True)
                    time.sleep(0.8)
                    placeholders["fertilizer"].markdown(f"<div class='agent-pipeline-node agent-complete'>✓ Fertilizer Advisor Agent: Formulating soil/NPK remedies...</div>", unsafe_allow_html=True)
                    
                    # Step 5: Market
                    placeholders["market"].markdown(f"<div class='agent-pipeline-node agent-active'>⏳ Market Agent: Retrieving commodity pricing and opportunity projections...</div>", unsafe_allow_html=True)
                    time.sleep(0.8)
                    placeholders["market"].markdown(f"<div class='agent-pipeline-node agent-complete'>✓ Market Agent: Retrieving commodity pricing and opportunity projections...</div>", unsafe_allow_html=True)
                    
                    # Step 6: Planner
                    placeholders["planner"].markdown(f"<div class='agent-pipeline-node agent-active'>⏳ Farm Planner Agent: Compiling calendar recovery tasks...</div>", unsafe_allow_html=True)
                    time.sleep(0.8)
                    placeholders["planner"].markdown(f"<div class='agent-pipeline-node agent-complete'>✓ Farm Planner Agent: Compiling calendar recovery tasks...</div>", unsafe_allow_html=True)
                    
                    # Step 7: Translator
                    placeholders["translator"].markdown(f"<div class='agent-pipeline-node agent-active'>⏳ Nepali Agent: Translating agricultural summaries to Nepali...</div>", unsafe_allow_html=True)
                    time.sleep(0.8)
                    placeholders["translator"].markdown(f"<div class='agent-pipeline-node agent-complete'>✓ Nepali Agent: Translating agricultural summaries to Nepali...</div>", unsafe_allow_html=True)
                    
                    # Run the actual backend code execution
                    result = st.session_state.orchestrator.execute_antigravity_workflow(
                        image_path=active_image_path,
                        symptoms_text=symptoms_text,
                        location=location_inp,
                        user=st.session_state.user_id,
                        role=st.session_state.role
                    )
                    
                    # Step 8: Orchestrator Compile
                    placeholders["orchestrator_compile"].markdown(f"<div class='agent-pipeline-node agent-active'>⏳ Orchestrator Agent: Finalizing farm directive report...</div>", unsafe_allow_html=True)
                    time.sleep(0.6)
                    placeholders["orchestrator_compile"].markdown(f"<div class='agent-pipeline-node agent-complete'>✓ Orchestrator Agent: Finalizing farm directive report...</div>", unsafe_allow_html=True)
                    
                    st.success("⚡ Autonomous Multi-Agent Chain Executed Successfully!")
                    
                    # Store report for tabs integration
                    st.session_state.active_report = result
                    
                    # Render synthesized summary with Output Safety Filter
                    safe_summary = filter_agent_output(result["summary"], st.session_state.user_id, st.session_state.role)
                    st.markdown("### 📋 Executive Summary")
                    st.markdown(safe_summary)
                    
                    # Render translated summary
                    st.markdown("### 🇳🇵 नेपाली अनुवाद (Nepali Translation)")
                    st.markdown(result["nepali_translation"])
                    
                    # Download Report button
                    st.download_button(
                        label="Download Full Agricultural Intelligence Report (Markdown)",
                        data=result["final_report"],
                        file_name=f"agrisathi_farm_report_{result['diagnostics']['crop'].lower()}.md",
                        mime="text/markdown"
                    )

    # --- TAB 3: MARKET FORECASTING ---
    with t_market:
        st.markdown("### Market Price Trends & Forecasting")
        st.caption("Accessing commodity transaction records and historical curves from the Market MCP tool.")
        
        crop_sel = st.selectbox("Select Target Crop", ["Tomato", "Rice", "Potato", "Maize", "Cardamom"])
        district_sel = st.text_input("Enter Market District", value="Kathmandu")
        
        if st.button("Fetch Market Forecast"):
            with st.spinner("Retrieving price tables from Market MCP..."):
                market_data = st.session_state.orchestrator.market_agent.run(crop_sel, district_sel)
                st.markdown(market_data["current_prices"])
                st.markdown(market_data["trends"])
                
                # Render beautiful Interactive Trend Graph using Plotly
                try:
                    conn = sqlite3.connect(DB_PATH)
                    df = pd.read_sql_query(
                        "SELECT month, avg_price FROM market_trends WHERE LOWER(crop) = LOWER(?)", 
                        conn, 
                        params=[crop_sel]
                    )
                    conn.close()
                    
                    # Month sorter mapping
                    month_map = {'Jan':1, 'Feb':2, 'Mar':3, 'Apr':4, 'May':5, 'Jun':6, 'Jul':7, 'Aug':8, 'Sep':9, 'Oct':10, 'Nov':11, 'Dec':12}
                    df['month_idx'] = df['month'].map(month_map)
                    df = df.sort_values('month_idx')
                    
                    if not df.empty:
                        st.markdown("#### 12-Month Historical Price Curve")
                        fig = px.line(
                            df, 
                            x="month", 
                            y="avg_price", 
                            labels={"month": "Month", "avg_price": "Average Price (NPR/kg)"},
                            title=f"Seasonality price curve for {crop_sel}",
                            markers=True
                        )
                        # Styled layout for chart
                        fig.update_layout(
                            plot_bgcolor='rgba(0,0,0,0)',
                            paper_bgcolor='rgba(0,0,0,0)',
                            font_color='#a0aec0',
                            xaxis=dict(showgrid=False),
                            yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)')
                        )
                        fig.update_traces(line_color='#38ef7d', marker=dict(size=8, color='#11998e'))
                        st.plotly_chart(fig, use_container_width=True)
                except Exception as ex:
                    st.caption(f"Could not load graphical trend line: {ex}")

    # --- TAB 4: FARM CALENDAR ---
    with t_calendar:
        st.markdown("### Interactive Farm Calendar & Checklists")
        st.caption("Seasonal recovery milestone tasks structured by the Farm Planner agent.")
        
        # Load from active report session state if exists
        if "active_report" in st.session_state and st.session_state.active_report:
            report_data = st.session_state.active_report
            plan_data = report_data["plan"]
            
            st.markdown(f"🎯 **Milestone Goal:** {plan_data['milestone']}")
            
            # Interactive task checklist
            for week_info in plan_data["schedule"]:
                st.markdown(f"#### 📅 {week_info['week']}")
                for task in week_info["tasks"]:
                    task_id = f"task_{week_info['week']}_{task[:20]}"
                    st.checkbox(task, key=task_id)
        else:
            st.info("No active recovery plan is currently loaded. Please run the **Crop Doctor** diagnostics page with an image/symptom case to generate a customized calendar.")
            
            # Simple Default Calendar
            st.markdown("#### Standard Seasonal Maintenance Checklist")
            st.checkbox("Check soil moisture daily at base layer")
            st.checkbox("Scout leaf undersides for fungal or pest larvae")
            st.checkbox("Apply compost/mulch layer to retain humidity controls")

    # --- TAB 5: SECURITY & AUDIT LOG ---
    with t_security:
        st.markdown("### Governance, Threat Defense & Audit Logs")
        
        # RBAC Check: Only Admin can see full logs; Advisor sees summaries; Farmer is restricted
        if not has_permission(st.session_state.role, "Advisor"):
            st.error("🚫 Access Denied: You must be an 'Advisor' or 'Admin' to view audit trails. General Farmer roles are restricted.")
        else:
            st.success("✓ Access Granted: Authorized Role level detected.")
            
            # Security Parameters Overview
            st.markdown("#### active Guard Systems")
            sc1, sc2, sc3 = st.columns(3)
            with sc1:
                st.info("**Prompt Injection Defense:** Active\n- Threshold: Strict regex signatures\n- Actions: Terminate execution, Log alert")
            with sc2:
                st.info("**Chemical Safety Filter:** Active\n- Scope: Banned substances redactor\n- Actions: Append safety disclaimers")
            with sc3:
                st.info("**Tool Execution Control:** Active\n- Scope: RBAC verification\n- Actions: Explicit user consent checks")
                
            # Audit Logs Database Viewer (Only Admin sees detailed DB rows)
            if st.session_state.role == "Admin":
                st.markdown("#### Real-time Audit Logs Database (`agrisathi.db`)")
                logs = get_audit_logs(limit=50)
                if logs:
                    df_logs = pd.DataFrame(logs, columns=["Timestamp", "User", "Role", "Action", "Details", "Status"])
                    
                    # Style rows based on security status
                    def color_status(val):
                        if val == "BLOCKED":
                            return "background-color: rgba(245, 101, 101, 0.2); color: #f56565;"
                        elif val == "WARN":
                            return "background-color: rgba(237, 137, 54, 0.2); color: #ed8936;"
                        return ""
                    
                    st.dataframe(df_logs, use_container_width=True)
                else:
                    st.info("No audit logs in database yet.")
            else:
                st.markdown("#### Real-time Audit Summary")
                st.caption("Advisor role access displays summary statistics only. Database record grid is restricted to Administrators.")
                logs = get_audit_logs(limit=50)
                if logs:
                    total_events = len(logs)
                    blocks = sum(1 for log in logs if log[5] == "BLOCKED")
                    warns = sum(1 for log in logs if log[5] == "WARN")
                    
                    st.metric("Total Events Logged", total_events)
                    st.metric("Threats / Prompt Injections Blocked", blocks)
                    st.metric("Pesticide Redactions / Warnings Triggered", warns)
                else:
                    st.caption("No events recorded.")
