# AgriSathi AI - Architectural Overview

This document details the multi-agent system design, Model Context Protocol (MCP) integrations, and security frameworks of **AgriSathi AI**.

---

## 1. System Architecture

AgriSathi AI is built as a modular, containerized application with a tiered design:

```
┌────────────────────────────────────────────────────────┐
│                   Streamlit Web UI                     │
│    (Chat, Vision Doctor, Market charts, Calendar)      │
└───────────────────────────┬────────────────────────────┘
                            │
┌───────────────────────────▼────────────────────────────┐
│              Google ADK Orchestrator Agent             │
│   (State management, Conversation Memory, Coordination)│
└───────────────────────────┬────────────────────────────┘
                            │
          ┌─────────────────┼─────────────────┐
          ▼                 ▼                 ▼
   ┌─────────────┐   ┌─────────────┐   ┌─────────────┐
   │ Crop Doctor │   │Weather Agent│   │Market Agent │
   │   Agent     │   │    Agent    │   │    Agent    │
   └──────┬──────┘   └──────┬──────┘   └──────┬──────┘
          │                 │                 │
          └─────────────────┼─────────────────┘
                            │ (Chained Execution)
          ┌─────────────────┼─────────────────┐
          ▼                 ▼                 ▼
   ┌─────────────┐   ┌─────────────┐   ┌─────────────┐
   │ Fertilizer  │   │Farm Planner │   │Nepali Lang  │
   │    Agent    │   │    Agent    │   │    Agent    │
   └──────┬──────┘   └──────┬──────┘   └──────┬──────┘
          │                 │                 │
          └─────────────────┴─────────────────┘
                            │
┌───────────────────────────▼────────────────────────────┐
│               Model Context Protocol (MCP)             │
│    (Weather MCP, Market price MCP, Crop Knowledge MCP) │
└───────────────────────────┬────────────────────────────┘
                            │
┌───────────────────────────▼────────────────────────────┐
│                    SQLite Database                     │
│         (Pricing data, Pathology lists, Audits)        │
└────────────────────────────────────────────────────────┘
```

---

## 2. Multi-Agent Design (Google ADK)

1. **Orchestrator Agent**: Extends the central ADK agent class, acting as the main state coordinator. It chains the output of pathology diagnostics to weather forecasting, nutrient calculations, economic impacts, task schedulers, and Nepali translators.
2. **Crop Doctor Agent**: Focuses on plant pathology. It accepts leaf image file artifacts and translates raw pixels into classified diseases, confidence scores, and raw treatment lists.
3. **Weather Intelligence Agent**: Communicates with the Weather MCP server to extract environmental risk boundaries.
4. **Fertilizer Advisor Agent**: Translates disease diagnostics and soil conditions into target N-P-K fertilizer schedules, focusing on organic companion techniques.
5. **Market Intelligence Agent**: Assesses regional sales windows and profitability indicators based on transaction records.
6. **Farm Planner Agent**: Creates 4-week task calendars representing actionable milestones for farm rehabilitation.
7. **Nepali Language Agent**: Receives text directives and localizes them into voice-friendly, simplified Nepalese sentences.

---

## 3. Model Context Protocol (MCP) Integration

Tools are exposed via 3 specialized FastMCP servers:
- **Weather Server (`weather_mcp.py`)**: Exposes `get_forecast` and `assess_weather_risks`. It runs temperature/humidity checks to flag fungal (blight, blast) or thermal (frost, heat stress) alerts.
- **Market Server (`market_mcp.py`)**: Exposes `get_crop_price` and `analyze_market_trends`. Connects to SQLite database to query current commodity averages and month-by-month pricing seasonality.
- **Knowledge Server (`knowledge_mcp.py`)**: Exposes `search_disease_db` and `get_treatment_plan`. Exposes diagnostic references and chemical/organic crop remedies.

---

## 4. Multi-Layer Security & Governance

The platform features a multi-tiered security pattern built to prevent abuse and protect farmers:

- **Authentication & RBAC**: Passcode authentication separates access privileges (Farmer, Advisor, Admin).
- **Prompt Injection Defense**: Prevents instruction-override attacks by analyzing chat strings against jailbreak patterns.
- **Tool Permission Governance**: Enforces explicit user consent checklists in the UI before execute-write tools are allowed to operate.
- **Input Validation**: Sanitizes file attachments, blocking files that exceed 5MB or carry non-image file extensions.
- **Safe Response Filter**: Reviews LLM responses to block toxic statements or banned pesticide recommendations.
- **Audit Logging**: Inserts audit details directly into SQLite database logs, enabling transparent accountability.
