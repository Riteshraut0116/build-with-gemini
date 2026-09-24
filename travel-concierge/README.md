# ✈️ Travel & Adventure Concierge

![Demo](agent_demo.gif)

A conversational AI agent built with Google's Agent Development Kit (ADK) that acts as a personalized travel planner. Travel & Adventure Concierge helps users discover destinations, plan trips, calculate budgets, and even generates stunning postcards and cinematic videos for your next vacation!

## ✨ Features

The agent is wired up with several Google Cloud services and custom tools to handle complex travel workflows:

- **🧠 Personalized Memory (Vertex AI Memory Bank)**: Automatically remembers your traveler preferences, dietary needs, budget tier, and past visited cities across conversations.
- **🗄️ Destination Catalog (Firestore)**: Look up and search through a rich database of travel destinations.
- **🖼️ Postcard Generation (Gemini 3.1 Flash Lite Image)**: Generates custom preview photos and artwork for destinations and uploads them to Google Cloud Storage.
- **🎥 Cinematic Videos (Gemini Omni Flash Preview)**: Generates stunning 2-second drone shots and cinematic clips of landmarks, directly saved to Cloud Storage.
- **🧮 Budget Sandbox Math**: Leverages a secure Python Code Execution Sandbox to run complex multi-step math (like daily expense splits, currency conversions, discount applications, and tax additions) reliably.
- **🛠️ Integrated API Tools**:
  - `convert_currency`: Real-time foreign exchange rates (via Frankfurter API).
  - `get_live_weather`: Live temperature and weather forecasts worldwide (via Open-Meteo).
  - `geocode_address` & `find_nearby_places`: Discover local cafes, restaurants, and attractions using Google Maps APIs.
  - `get_current_time`: Check local timezones for major cities.
- **🎨 Interactive UI (A2UI)**: Renders beautiful chat dialogue with dynamic interactive chips, light/dark mode, and rich image lightboxes.

### 🚧 Planned (Not Yet Implemented)
- *Itinerary Generator Tool* (Currently relies on standard LLM generation).
- *Hotel booking tables and widgets* (Currently tables are unsupported in the UI).

## 🗂️ Repository Structure

```text
.
├── app/
│   ├── agent.py               # Core ADK agent definition, tools, and prompts
│   ├── a2ui_utils.py          # A2UI callback and rendering helpers
│   ├── fast_api_app.py        # ADK FastAPI entrypoint for the agent
│   └── app_utils/             # Helpers for reasoning engine and telemetry
├── frontend/
│   ├── main.py                # Custom proxy server bridging local UI to Agent Runtime
│   ├── static/
│   │   └── index.html         # Custom Travel & Adventure Concierge web UI
│   └── requirements.txt       # Frontend Python dependencies
├── deployment/                # Terraform IaC definitions for GCP resources
├── tests/                     # Unit, integration, and agent evaluation tests
├── .agents/                   # Custom skills and agents-cli configuration
├── pyproject.toml             # Python project dependencies (managed by uv)
├── Dockerfile                 # Containerization for deployment
├── GEMINI.md                  # Agent System Instructions
└── agents-cli-manifest.yaml   # Agents CLI configuration and metadata
```

## 🛠️ Tech Stack & Skills

- **Languages**: Python (Backend Agent & Proxy), HTML / CSS / JavaScript (Frontend UI).
- **Framework**: Google Agent Development Kit (ADK).
- **Core AI Models**: Gemini 2.5 Flash (Reasoning), Gemini 3.1 Flash Lite Image (Images), Gemini Omni Flash Preview (Video).
- **Google Cloud Platform**: Vertex AI Agent Runtime, Memory Bank, Firestore, Cloud Storage, Cloud Run.
- **External APIs**: Open-Meteo (Weather), Frankfurter (Currency), Google Maps Platform (Places & Geocoding).

## 🚀 How to Run Locally

You can spin up the agent and its custom frontend proxy locally using the following commands:

1. **Start the Agent Playground (Backend)**:
   ```bash
   uv tool run google-agents-cli playground
   ```
2. **Start the Custom Frontend (Proxy)**:
   In a separate terminal, navigate to the `frontend/` directory and run the proxy server:
   ```bash
   cd frontend
   uv run python main.py
   ```
3. Open your browser to `http://localhost:8080` and start planning your adventure!
