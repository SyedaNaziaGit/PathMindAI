# PathMindAI

**A multi-agent AI travel planning system built with LangGraph, MCP, and real-time APIs.**

PathMindAI takes a natural-language trip request, splits it across specialised AI agents (flights, weather, destination research, itinerary), and returns a complete, budget-aware travel plan.

>  **Status:** Backend is working; the Streamlit frontend is still under active development.

---

## Overview

Planning a trip means juggling flights, weather, places to visit, and budget across many tabs. PathMindAI coordinates multiple LLM-powered agents through a **LangGraph** state graph. Each agent owns one job and calls external tools through **MCP (Model Context Protocol)** servers and REST APIs, so the final answer is based on live data rather than model memory.

## Features

- **Multi-agent orchestration** with LangGraph (shared graph state, routing between agents)
- **MCP integrations** for tool access (flight data, weather)
- **Live web search** via Tavily for destinations, hotels, and sightseeing
- **Real-time flight information** via AviationStack
- **Weather forecasts** via OpenWeatherMap
- **Streamlit chat UI** for interactive planning *(in progress)*
- **Persistent memory** with PostgreSQL checkpointing <!-- VERIFY: keep only if implemented -->
- **Supervisor agent, guardrails, human-in-the-loop** <!-- VERIFY: keep only if implemented -->

## Architecture

```
                    ┌──────────────────────┐
   User request ──▶ │   Streamlit Frontend │
                    └──────────┬───────────┘
                               ▼
                    ┌──────────────────────┐
                    │  LangGraph Backend   │
                    │  (shared graph state)│
                    └──────────┬───────────┘
                               ▼
        ┌──────────────┬───────┴───────┬──────────────┐
        ▼              ▼               ▼              ▼
   Flight Agent   Weather Agent   Search Agent   Itinerary Agent
        │              │               │              │
        ▼              ▼               ▼              ▼
  AviationStack    Weather MCP     Tavily API    Final plan built
   MCP server        server                      from agent outputs
```

<!-- VERIFY: rename the agents above to match the files in /agents -->

**Flow:** the user prompt enters the graph → state is passed between agents → each agent calls its tools (MCP or API) → results are merged into one structured trip plan → the plan is shown in the UI.

## Project Structure

```
PathMindAI/
├── agents/                 # Individual agent definitions and prompts
├── config.py               # Environment variables, model and API configuration
├── graph_state.py          # Shared LangGraph state schema
├── langgraph_backend.py    # Graph construction, routing, and execution
├── mcp_clients.py          # MCP client setup for external tool servers
├── streamlit_frontend.py   # Streamlit web interface
├── requirements.txt        # Python dependencies
├── .gitignore
└── README.md
```

## Tech Stack

| Layer | Technology |
|---|---|
| Language | Python |
| Agent orchestration | LangGraph, LangChain |
| LLM provider | Groq <!-- VERIFY: or OpenAI, etc. --> |
| Tool protocol | MCP (Model Context Protocol) |
| Search | Tavily |
| Flights | AviationStack |
| Weather | OpenWeatherMap |
| Memory (optional) | PostgreSQL + LangGraph checkpointer |
| Frontend | Streamlit |

## Prerequisites

**API keys**

- Groq: <https://console.groq.com>
- Tavily: <https://www.tavily.com/>
- AviationStack: <https://aviationstack.com/>
- OpenWeatherMap: <https://openweathermap.org/>

**Tools**

- Python 3.10+
- Git
- [uv](https://docs.astral.sh/uv/) (to run the AviationStack MCP server)
- PostgreSQL, if persistent memory is enabled: <https://www.postgresql.org/download/>

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/SyedaNaziaGit/PathMindAI.git
cd PathMindAI
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
```

Windows:

```bash
venv\Scripts\activate
```

macOS / Linux:

```bash
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key
TAVILY_API_KEY=your_tavily_api_key
AVIATIONSTACK_API_KEY=your_aviationstack_api_key
OPENWEATHER_API_KEY=your_openweathermap_api_key

# Only if PostgreSQL memory is enabled
DATABASE_URL=postgresql://postgres:your_password@localhost:5432/pathmindai
```

> ⚠️ Never commit your `.env` file. It is already covered by `.gitignore`; double-check before pushing.

### 5. (Optional) Create the PostgreSQL database

```sql
CREATE DATABASE pathmindai;
```

Note the password and port you chose during PostgreSQL installation and use them in `DATABASE_URL`.

## MCP Servers

### AviationStack MCP (flight data)

Uses the open-source [aviationstack-mcp](https://github.com/Pradumnasaraf/aviationstack-mcp) server.

```bash
git clone https://github.com/Pradumnasaraf/aviationstack-mcp.git
cd aviationstack-mcp
```

Create a `.env` inside that folder:

```env
AVIATION_STACK_API_KEY=your_api_key_here
```

Install and start:

```bash
uv sync
uv run -m aviationstack_mcp mcp run
```

Keep this terminal open; the server waits for MCP requests. Stop it with `Ctrl + C`.

### Weather MCP

Make sure your OpenWeatherMap key is in `.env`, then install the dependencies:

```bash
pip install mcp requests
```

### Tavily

Tavily is used for live web search. See the [Tavily MCP docs](https://docs.tavily.com/documentation/mcp) if you want to run it as an MCP server.

## Running the App

Start the required MCP server(s) first, then in the project root:

```bash
streamlit run streamlit_frontend.py
```

The app opens at `http://localhost:8501`.

## Example Prompts

```
Plan a complete 7-day Japan trip including flights, hotels and sightseeing under ₹2 lakhs.
```

```
Find flights from Bengaluru to Berlin next month and tell me the weather on arrival.
```

```
Suggest a 3-day weekend itinerary in Goa on a budget of ₹15,000.
```


---

⭐ If you find this project useful, consider giving it a star
