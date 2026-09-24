<br>

<div align="center">

<img src="assets/build-with-gemini-banner.png" alt="Build with Gemini" width="100%" />

# 🚀 Build with Gemini

## ✈️ Travel & Adventure Concierge

### 🌍 Plan smarter. Explore farther. Remember every adventure.

</div>

<br>

<p align="center">

![Google ADK](https://img.shields.io/badge/Google-Agent%20Development%20Kit-4285F4?logo=google)
![Gemini](https://img.shields.io/badge/Google-Gemini-8E75B2?logo=googlegemini)
![Vertex AI](https://img.shields.io/badge/Google%20Cloud-Vertex%20AI-4285F4?logo=googlecloud)
![Architecture](https://img.shields.io/badge/Architecture-Agentic%20AI-orange)
![Infrastructure](https://img.shields.io/badge/Infrastructure-Terraform-7B42BC?logo=terraform)
![Deployment](https://img.shields.io/badge/Deployment-Cloud%20Native-success)

</p>

---

# 🎯 Project Overview

**Travel & Adventure Concierge** is a conversational, cloud-native AI travel agent built with **Google's Agent Development Kit (ADK)**. It helps users discover destinations, plan trips, calculate travel budgets, find nearby places, check live conditions, and generate personalized travel media through a rich interactive experience.

The agent combines **Gemini models, Vertex AI Agent Runtime, Memory Bank, Firestore, Cloud Storage, Cloud Run, secure Python code execution, and external travel APIs** to support complex, multi-step travel workflows.

![Demo](agent_demo.gif)

---

# 🚨 Problem Statement

Travel planning often requires users to switch between multiple applications and manually combine information related to:

- 🌍 Destination discovery
- 💰 Budget planning and currency conversion
- 🌦️ Live weather conditions
- 📍 Nearby restaurants, cafés, and attractions
- 🕒 Local time zones
- 🧠 Personal preferences and previous trips
- 🖼️ Visual destination previews

This fragmented process makes trip research repetitive and difficult to personalize across conversations.

---

# 💡 Proposed Solution

The **Travel & Adventure Concierge** brings travel discovery, planning, calculations, contextual memory, real-time information, and generative media into one conversational AI experience.

Users can interact naturally with an agent that:

🔎 Searches a structured destination catalog

🧠 Remembers traveler preferences across conversations

💱 Converts currencies using real-time exchange-rate data

🌦️ Retrieves live weather forecasts

📍 Discovers nearby places using maps and geocoding tools

🧮 Performs reliable multi-step travel budget calculations

🖼️ Generates destination postcards and preview artwork

🎥 Creates short cinematic travel clips

---

# 🎯 Objectives

- ✅ Simplify destination research and trip planning
- ✅ Personalize recommendations using persistent traveler memory
- ✅ Provide live travel context through integrated APIs
- ✅ Improve budget calculation reliability using secure code execution
- ✅ Create engaging travel previews using generative media
- ✅ Deliver an interactive, responsive user experience
- ✅ Support cloud-native deployment and infrastructure automation

---

# 🏗️ Solution Architecture

## High-Level Architecture

```text
Traveler
   │
   ▼
Interactive A2UI Web Experience
   │
   ▼
Frontend Proxy Server
   │
   ▼
Google Agent Development Kit (ADK)
   │
   ├── Gemini 2.5 Flash
   ├── Vertex AI Memory Bank
   ├── Firestore Destination Catalog
   ├── Secure Python Code Execution Sandbox
   ├── Travel API Tools
   ├── Gemini Image Generation
   └── Gemini Video Generation
             │
             ▼
Google Cloud Storage + Vertex AI Agent Runtime
             │
             ▼
Cloud Run Deployment
```

---

# 🔍 Architecture Components

## 🤖 Google Agent Development Kit (ADK)

Acts as the core agent framework and coordinates prompts, tools, memory, and travel workflows.

### Responsibilities

- Agent definition and orchestration
- Tool selection and execution
- Prompt and instruction handling
- Multi-step travel workflow coordination
- Integration with the custom frontend

---

## 🧠 Gemini 2.5 Flash

Provides the core reasoning capability for conversational trip planning and travel assistance.

### Responsibilities

- Natural language understanding
- Destination and itinerary guidance
- Context-aware travel responses
- Coordination of available tools

---

## 💾 Vertex AI Memory Bank

Maintains personalized traveler context across conversations.

### Remembers

- Traveler preferences
- Dietary requirements
- Budget tier
- Previously visited cities

---

## 🗄️ Firestore

Provides the destination catalog used to look up and search travel destinations.

---

## 🧮 Secure Python Code Execution Sandbox

Runs deterministic, multi-step travel calculations.

### Example Calculations

- Daily expense splits
- Currency conversions
- Discount applications
- Tax additions
- Multi-stage budget calculations

---

## 🖼️ Gemini 3.1 Flash Lite Image

Generates personalized destination preview images, artwork, and postcards. Generated assets are uploaded to **Google Cloud Storage**.

---

## 🎥 Gemini Omni Flash Preview

Generates short, two-second drone-style shots and cinematic destination clips, which are saved to **Google Cloud Storage**.

---

## 🎨 A2UI Interactive Experience

Provides a polished conversational interface with:

- Dynamic interactive chips
- Light and dark modes
- Rich image lightboxes
- Travel-focused dialogue presentation

---

# 🛠️ Integrated Travel Tools

| Tool | Purpose |
|------|---------|
| `convert_currency` | Retrieves real-time foreign exchange rates through the Frankfurter API |
| `get_live_weather` | Retrieves live temperatures and worldwide weather forecasts through Open-Meteo |
| `geocode_address` | Converts an address or destination into geographic coordinates |
| `find_nearby_places` | Finds nearby cafés, restaurants, attractions, and other places through Google Maps APIs |
| `get_current_time` | Returns local time information for major cities |

---

# 🚀 Execution Flow

## Step 1

💬 The traveler submits a natural-language request.

```text
Plan a budget-friendly trip and suggest nearby attractions.
```

## Step 2

🧠 The agent uses relevant stored preferences from **Vertex AI Memory Bank**.

## Step 3

🗄️ **Firestore** is queried when destination catalog information is needed.

## Step 4

🛠️ The agent invokes the appropriate tools for weather, currency, time, geocoding, nearby places, or budget calculations.

## Step 5

🖼️ Image or video models generate optional travel previews and store the generated assets in **Cloud Storage**.

## Step 6

✅ The interactive frontend presents the final travel guidance and media to the user.

---

# ✅ Key Features

## 🧠 Personalized Travel Memory

The agent remembers key preferences, dietary needs, budget tier, and previously visited cities across conversations.

## 🌍 Destination Discovery

A Firestore-backed catalog enables structured destination lookup and search.

## 💰 Budget Planning

The secure Python sandbox handles calculations such as expense splitting, conversions, discounts, and taxes.

## 🌦️ Live Travel Context

Integrated APIs provide current weather, currency exchange data, local time, and nearby place discovery.

## 🖼️ AI-Generated Postcards

The solution generates customized destination preview images and travel artwork.

## 🎥 Cinematic Destination Videos

The agent can create short cinematic clips and drone-style landmark previews.

## 🎨 Rich Interactive UI

A2UI supports interactive chips, responsive dialogue, light and dark themes, and image lightboxes.

---

# 📦 Project Structure

```text
Travel-and-Adventure-Concierge/
│
├── app/
│   ├── agent.py                 # Core ADK agent definition, tools, and prompts
│   ├── a2ui_utils.py            # A2UI callbacks and rendering helpers
│   ├── fast_api_app.py          # ADK FastAPI entry point
│   └── app_utils/               # Reasoning engine and telemetry helpers
│
├── frontend/
│   ├── main.py                  # Proxy bridging the local UI and Agent Runtime
│   ├── static/
│   │   └── index.html           # Custom travel concierge web interface
│   └── requirements.txt         # Frontend Python dependencies
│
├── deployment/                  # Terraform infrastructure definitions
├── tests/                       # Unit, integration, and agent evaluation tests
├── .agents/                     # Custom skills and agents-cli configuration
├── pyproject.toml               # Python dependencies managed by uv
├── Dockerfile                   # Application container definition
├── GEMINI.md                    # Agent system instructions
└── agents-cli-manifest.yaml     # Agents CLI configuration and metadata
```

---

# 🛠️ Technology Stack

| Category | Technology |
|----------|------------|
| Agent Framework | Google Agent Development Kit (ADK) |
| Reasoning Model | Gemini 2.5 Flash |
| Image Generation | Gemini 3.1 Flash Lite Image |
| Video Generation | Gemini Omni Flash Preview |
| Agent Runtime | Vertex AI Agent Runtime |
| Persistent Memory | Vertex AI Memory Bank |
| Database | Firestore |
| Object Storage | Google Cloud Storage |
| Deployment | Google Cloud Run |
| Backend | Python and FastAPI |
| Frontend | HTML, CSS, and JavaScript |
| Interactive UI | A2UI |
| Infrastructure as Code | Terraform |
| Package Management | uv |
| Weather Data | Open-Meteo |
| Currency Data | Frankfurter API |
| Maps and Places | Google Maps Platform |

---

# 💼 Business Value

| Capability | Value |
|------------|-------|
| Persistent traveler memory | More personalized interactions across conversations |
| Unified travel tools | Less switching between separate planning services |
| Budget sandbox | More reliable multi-step travel calculations |
| Live API integrations | Current weather, exchange-rate, time, and nearby-place context |
| Generative images and video | More engaging destination discovery and previews |
| Cloud-native architecture | Supports containerized deployment and infrastructure automation |
| Automated tests and evaluations | Supports solution quality across agent workflows |

---

# 🗺️ Current Scope and Planned Enhancements

## Implemented ✅

- Google ADK-based conversational agent
- Personalized memory through Vertex AI Memory Bank
- Firestore destination catalog
- AI postcard generation
- Short cinematic video generation
- Secure budget calculation sandbox
- Currency, weather, maps, geocoding, and local-time tools
- Custom interactive A2UI frontend
- Terraform deployment configuration
- Unit, integration, and agent evaluation tests

## Planned 🚧

- Dedicated itinerary generator tool
- Hotel booking tables and widgets

> **Note:** Itinerary creation currently relies on standard LLM generation, and the current UI does not support hotel booking tables or widgets.

---

# 💻 Run Locally

## Prerequisites

Ensure the project dependencies and required service configuration are available in your local environment.

## 1. Start the Agent Playground

```bash
uv tool run google-agents-cli playground
```

## 2. Start the Custom Frontend Proxy

Open a separate terminal and run:

```bash
cd frontend
uv run python main.py
```

## 3. Open the Application

Open the following address in your browser:

[Launch the local Travel & Adventure Concierge](http://localhost:8080)

---

# 🧪 Testing and Evaluation

The repository includes a `tests/` directory for:

- Unit tests
- Integration tests
- Agent evaluation tests

---

# 🚀 Deployment

The solution includes:

- A `Dockerfile` for containerization
- Terraform definitions under `deployment/`
- Google Cloud Run as the deployment platform
- Vertex AI Agent Runtime for agent execution
- Google Cloud Storage for generated media assets

---

# 🔮 Future Roadmap

## Phase 1: Core Agent Experience ✅

- Conversational travel assistance
- Destination lookup
- Persistent traveler memory
- Live travel API tools
- Budget calculation sandbox

## Phase 2: Generative Travel Media ✅

- Customized postcard generation
- Destination artwork
- Short cinematic travel videos
- Cloud-hosted generated assets

## Phase 3: Planning Enhancements 🚧

- Dedicated itinerary generator tool
- Structured hotel booking tables
- Interactive booking widgets

---

# 🌟 Key Differentiators

⭐ Persistent traveler memory across conversations

⭐ Real-time weather, currency, time, and place discovery

⭐ Secure Python-based budget calculations

⭐ Multimodal image and video generation

⭐ Interactive A2UI travel experience

⭐ Cloud-native and containerized architecture

⭐ Terraform-based infrastructure definitions

⭐ Built-in unit, integration, and agent evaluation testing

---

# 🙏 Acknowledgements

Built using **Google Agent Development Kit, Gemini, Vertex AI, Firestore, Cloud Storage, Cloud Run, Google Maps Platform, Open-Meteo, and Frankfurter API**.

Our mission is simple:

> ✈️ **Turn travel ideas into personalized adventures through one intelligent conversation.**

---

## 👤 Author

**Ritesh Raut**
*Associate, Cognizant*

## 🌍 Discover More. Plan Better. Travel Inspired.

---

### 🌐 Connect with me:
<p align="left">
<a href="https://github.com/Riteshraut0116" target="blank"><img align="center" src="https://raw.githubusercontent.com/rahuldkjain/github-profile-readme-generator/master/src/images/icons/Social/github.svg" alt="Riteshraut0116" height="30" width="40" /></a>
<a href="https://linkedin.com/in/ritesh-raut-9aa4b71ba" target="blank"><img align="center" src="https://raw.githubusercontent.com/rahuldkjain/github-profile-readme-generator/master/src/images/icons/Social/linked-in-alt.svg" alt="ritesh-raut-9aa4b71ba" height="30" width="40" /></a>
<a href="https://www.instagram.com/riteshraut1601/" target="blank"><img align="center" src="https://raw.githubusercontent.com/rahuldkjain/github-profile-readme-generator/master/src/images/icons/Social/instagram.svg" alt="riteshraut1601" height="30" width="40" /></a>
<a href="https://www.facebook.com/ritesh.raut.649321/" target="blank"><img align="center" src="https://raw.githubusercontent.com/rahuldkjain/github-profile-readme-generator/master/src/images/icons/Social/facebook.svg" alt="ritesh.raut.649321" height="30" width="40" /></a>
</p>

---
