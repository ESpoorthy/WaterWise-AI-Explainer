# WaterWise AI — Water Supply & Distribution Process Explainer Bot
**Project 26** | **Industry Domain: Water Utilities / Municipal Services**

---

## 1. Problem Statement & Scope

Water supply departments receive frequent consumer queries regarding water distribution schedules, pressure issues, and water safety guidelines. Technical explanations are often difficult for citizens to understand, leading customer service teams to handle repetitive informational inquiries. 

**WaterWise AI** is an educational civic Generative AI chatbot built with Streamlit and Google AI Studio (Gemini Flash). It translates complex municipal water engineering concepts—such as treatment phases, hydraulic distribution loops, elevated balancing tanks, pressure variations, and conservation strategies—into clear, structured, and approachable language for citizens.

### Strict Functional Scope & Operational Boundaries
- **Educational Explanations Only**: Explains water utility engineering, treatment steps, distribution hydraulics, pressure causes, and household water conservation.
- **No Live Supply Predictions**: Cannot predict or verify when water will arrive in a specific neighborhood or residence.
- **No Complaint Registration**: Cannot register municipal complaints, log service tickets, or dispatch repair crews.
- **No Infrastructure Control**: Cannot operate pumps, valves, meters, or SCADA telemetry systems.
- **Pre-Flight Safety Enforcement**: Application-side checks deterministically intercept operational requests before any API calls to Google Gen AI.

---

## 2. Implemented Features

1. **Civic-Technology Streamlit UI**:
   - Deep navy structural layout with teal and aqua accents.
   - Interactive topic cards for Water Treatment, Distribution, Pressure, and Conservation.
   - Suggested question chips including all mandatory assignment queries.
   - Session state conversation history with clear-conversation controls.
   - Visible public-information disclaimer clarifying that the bot is not connected to live municipal telemetry.

2. **Google Gen AI Integration (Gemini Flash)**:
   - Built using the official `google-genai` Python SDK (`from google import genai`).
   - Configurable model selection with `GEMINI_MODEL=gemini-3.6-flash` as default.
   - Supports `gemini-3.8-flash` and other compatible Gemini Flash models.
   - Structured explanation framework: *Simple Explanation*, *How It Works*, *Why It Matters*, and *Key Takeaway*.
   - Context window bounds preserving up to 10 recent messages to prevent runaway token usage.

3. **Deterministic Safety Engine**:
   - Pre-flight regex and intent safety validation.
   - Specific, respectful refusals for arrival predictions, complaint filings, and infrastructure commands.
   - Educational protection allowing general inquiries about schedules and complaint procedures (e.g., *"How do municipal water distribution schedules generally work?"*).
   - Defense against prompt injection, jailbreaking, and system prompt extraction.

4. **Zero-Credential Offline Learning Centre**:
   - Fully functional Knowledge Centre with process diagrams and stage-by-stage engineering breakdowns.
   - Verified offline educational reference answers for standard queries when running without an API key.
   - Municipal water glossary explaining terms like *Potable*, *Turbidity*, *Coagulation*, *Flocculation*, *Static Head*, *PRV*, and *SCADA*.

---

## 3. Technology Stack

- **Language**: Python 3.12+
- **Frontend / Framework**: Streamlit (1.65.0)
- **AI Engine**: Google AI Studio API via official `google-genai` SDK (2.29.0)
- **Default Model**: `gemini-3.6-flash` (configurable to `gemini-3.8-flash`)
- **Testing**: Pytest (9.1.1) including `streamlit.testing.v1.AppTest`
- **Environment Management**: Python `venv` and `python-dotenv`

---

## 4. Architecture & Directory Structure

```
WaterWise-AI-Explainer/
├── app.py                      # Main Streamlit application entrypoint
├── requirements.txt            # Lightweight dependency declarations
├── pytest.ini                  # Pytest configuration
├── .env.example                # Template for environment configuration
├── .gitignore                  # Prevents secrets, venv, and cache commits
├── README.md                   # Complete documentation
├── .streamlit/
│   └── config.toml             # Streamlit visual theme and server settings
├── waterwise/
│   ├── __init__.py             # Package initializer
│   ├── config.py               # API key lookup, model settings, and masked logging
│   ├── safety.py               # Deterministic pre-flight safety boundaries and refusals
│   ├── prompts.py              # System instructions, structured persona, and query templates
│   ├── knowledge.py            # Offline educational curriculum, diagrams, and glossary
│   ├── ai_service.py           # Gemini client lifecycle, generation, and error handling
│   └── ui.py                   # Custom CSS tokens, badges, and civic UI components
└── tests/
    ├── test_safety.py          # Safety boundary tests (allowed vs blocked, prompt injection)
    ├── test_ai_service.py      # Mocked Gemini SDK tests, bounds, and provider error handling
    ├── test_knowledge.py       # Knowledge curriculum and curated answers tests
    ├── test_ui.py              # UI tokens and prompt bound tests
    └── test_streamlit_app.py   # Streamlit AppTest end-to-end integration tests
```

---

## 5. Setup & Installation

### Option A: macOS Installation

1. Open Terminal and navigate to the project root:
   ```bash
   cd WaterWise-AI-Explainer
   ```

2. Create and activate a clean Python virtual environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. Install required packages:
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. Configure your API key (see Configuration section below).

5. Launch WaterWise AI:
   ```bash
   streamlit run app.py
   ```

---

### Option B: Windows Installation

1. Open Command Prompt or PowerShell and navigate to the project directory:
   ```cmd
   cd WaterWise-AI-Explainer
   ```

2. Create and activate a virtual environment:
   ```cmd
   python -m venv .venv
   .venv\Scripts\activate
   ```

3. Install dependencies:
   ```cmd
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. Configure your API key and launch:
   ```cmd
   streamlit run app.py
   ```

---

## 6. Secure Configuration (API Keys & Model Selection)

WaterWise AI supports configuration priority in the following order:
1. `GEMINI_API_KEY` environment variable.
2. `GEMINI_API_KEY` in `.streamlit/secrets.toml`.
3. `GOOGLE_API_KEY` fallback environment variable or Streamlit secret.

### Using `.env` (Recommended for Local Dev)
Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```
Edit `.env`:
```ini
GEMINI_API_KEY=your_actual_google_ai_studio_api_key_here
GEMINI_MODEL=gemini-3.6-flash
```

### Using Streamlit Secrets
Create `.streamlit/secrets.toml`:
```toml
GEMINI_API_KEY = "your_actual_google_ai_studio_api_key_here"
GEMINI_MODEL = "gemini-3.6-flash"
```

> **Security Note:** `.env` and `.streamlit/secrets.toml` are registered in `.gitignore` to prevent committing secrets to version control. If no API key is provided, the app will still start and operate in **Offline Learning Mode**.

### Supported Models
- `gemini-3.6-flash` (Default): Fast, concise, highly available for Google AI Studio projects.
- `gemini-3.8-flash`: Available if enabled on your Google AI Studio project.
- `gemini-2.5-flash`: Compatible fallback.

---

## 7. Running Automated Tests

All tests run locally without making billable Gemini API calls or requiring internet access:

```bash
pytest -v
```

To run a specific test suite:
```bash
pytest tests/test_safety.py -v
pytest tests/test_ai_service.py -v
pytest tests/test_streamlit_app.py -v
```

---

## 8. Demonstration Guide (Step-by-Step)

1. **Start the Application**: Run `streamlit run app.py` and open the local URL.
2. **Ask the 4 Required Assignment Questions**:
   - `Explain the water treatment process.`
   - `How does water distribution work?`
   - `What causes low water pressure?`
   - `What are some water conservation tips?`
3. **Verify Prohibited Operational Requests (Safety Engine Intercepts)**:
   - Query: `When will the water supply arrive in my area?`
     - *Expected Outcome*: Intercepted before Gemini invocation; outputs standard refusal advising checking local utility schedules.
   - Query: `Register a complaint about low water pressure.`
     - *Expected Outcome*: Intercepted before Gemini invocation; outputs refusal stating bot cannot register complaints or dispatch crews.
4. **Verify Allowed Educational Questions on Similar Topics**:
   - Query: `How do municipal water distribution schedules generally work?`
     - *Expected Outcome*: Allowed; explains zoning, hydraulic balancing, and intermittent supply principles.
   - Query: `How do water utilities generally handle complaints?`
     - *Expected Outcome*: Allowed; explains how utilities trace pipe telemetry, isolate leaks, and log work orders.
5. **Explore Knowledge Centre**:
   - Navigate to the **Knowledge Centre** tab to view ASCII process diagrams, detailed stages, and FAQs.
6. **Test Clear Conversation**:
   - Click **Clear Conversation** in the sidebar to reset session state.

---

## 9. Deployment Instructions

To deploy to Streamlit Community Cloud:
1. Push this repository to GitHub (ensure `.env` and `.streamlit/secrets.toml` are NOT included).
2. Go to [share.streamlit.io](https://share.streamlit.io/) and select the repository.
3. Under **Advanced Settings > Secrets**, paste:
   ```toml
   GEMINI_API_KEY = "your_google_ai_studio_api_key"
   GEMINI_MODEL = "gemini-3.6-flash"
   ```
4. Click **Deploy**.
