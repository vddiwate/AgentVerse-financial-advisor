# AgentVerse

**AI-Powered Financial Portfolio Advisor** — a multi-agent system built with LangGraph,Langchain,FastAPI,and RAG.

AgentVerse gives users a single conversational assistant that understands their live portfolio, current market news, and their own uploaded financial documents — instead of making them piece all of that together manually across separate apps.

---

## Problem Statement

Retail investors typically manage their financial life across disconnected tools — a brokerage app for holdings, a news app for market updates, and PDF statements saved somewhere on their laptop. Answering "how am I really doing, and what should I do next?" means manually synthesizing all of this, which is slow and easy to get wrong for a non-expert.

AgentVerse solves this with one conversational assistant that already has access to all three sources and can reason across them to give a single, explainable answer.

---

## How It Works

A query enters through the API, is classified by a Supervisor node, routed to the relevant specialist agent(s), executed through a dedicated Tools layer, and synthesized into one final response by an Advisory agent.

```
API Layer → Supervisor Node → Routing Decision → Specialist Agent(s) → Tools Layer → Advisory Agent → API Layer
```

- The **Supervisor** classifies intent and decides which agent(s) are needed.
- **Agents** never call external APIs directly — they decide *which tool* to call.
- The **Tools Layer** (plain Python functions) is what actually makes HTTP requests to external services or queries the database.
- The **Advisory Agent** always runs last, synthesizing whatever context was gathered into one coherent response.

See `AgentVerse_LLD_Document.pdf` in this repo for the full architecture, sequence diagrams, database schema, and API design.

---

## Agents & Tools

| Agent | Responsibility | Tools |
|---|---|---|
| Supervisor / Router | Classifies intent, loads short-term memory | `classify_intent()` |
| Portfolio Analyzer | Portfolio value, gains/losses, sector exposure | `get_stock_price()`, `calculate_portfolio_returns()` |
| Market News | Recent news relevant to holdings | `fetch_latest_news()` |
| Document (RAG) | Answers grounded in the user's own documents | `search_personal_documents()` |
| Advisory | Final synthesis into one recommendation | `generate_recommendation()` |

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Streamlit + Plotly |
| Backend API | FastAPI + Uvicorn |
| Orchestration | LangGraph + LangChain |
| LLM (reasoning) | OpenAI / Groq API (`llama-3.3-70b-versatile`) |
| Embeddings | Hugging Face sentence-transformers (local) |
| Vector Database | ChromaDB (local, persistent) |
| Relational Database | PostgreSQL + SQLAlchemy ORM |
| Live Stock Data | Finnhub API |
| Live News Data | NewsAPI.org |
| Caching | cachetools (in-memory TTL cache) |
| Logging | Loguru (Structured async-safe logging, 2-day retention) |

---

## Project Structure

```
agentverse/
├── agentverse_backend/          # Main Backend package
│   ├── main.py                  # FastAPI app entrypoint
│   ├── config.py                # Pydantic Settings env loader
│   ├── api/                     # versioned endpoints
│   ├── agents/                  # LangGraph orchestrator & agent nodes
│   ├── registry/                # Decorator-based registries (agent, tool, prompt)
│   ├── tools/                   # External API tools & mocks
│   ├── services/                # Business logic layer
│   ├── utils/                   # Shared utilities (logger)
│   ├── schemas/                 # Pydantic requests/response validation
│   ├── db/                      # Database configuration
│   │   ├── database.py          # SQLAlchemy engine and session dependency
│   │   ├── models/              # Modular ORM Models package (agent, tool, prompt, etc.)
│   │   ├── init_db.py           # DB tables initialization script
│   │   ├── seed_data.json       # JSON file holding dynamic seed data
│   │   └── seed.py              # Seeding engine script
│   └── logs/                    # Automated local logs directory
├── alembic/                     # Alembic database migration scripts
│   ├── env.py                   # Alembic dynamic configuration
│   └── versions/                # Migration history scripts
├── alembic.ini                  # Alembic configurations
├── requirements.txt             # Project dependencies checklist
├── .env                         # Environment credentials (excluded from git)
├── .gitignore                   # Exclusions list for git commits
└── README.md
```

---

## Getting Started

### Prerequisites
- Python 3.10+
- PostgreSQL (local install or via Docker)
- API keys: Groq (or OpenAI), Finnhub, NewsAPI.org (all have free tiers)

### 1. Clone and set up environment variables
```bash
git clone <repo-url>
cd AgentVerse
# create .env in the root and fill in database configurations
# e.g.:
# GROQ_API_KEY=your_groq_api_key
# DB_USER=postgres
# DB_PASSWORD=your_password
# DB_HOST=localhost
# DB_PORT=5432
# DB_NAME=agentverse
```

### 2. Backend Environment Setup
```bash
# Initialize virtual environment
python -m venv venv
source venv/bin/activate        # Windows (Powershell): .\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 3. Database Migration & Initialization
We use **Alembic** to track database schema migrations and run PostgreSQL table setups:
```bash
# 1. Verify and apply migrations
.\venv\Scripts\alembic upgrade head

# 2. (Optional) Run seeding engine to populate default tools, agents & prompts
.\venv\Scripts\python agentverse_backend/db/seed.py
```

### 4. Run Backend Server
```bash
.\venv\Scripts\uvicorn agentverse_backend.main:app --reload --port 8000
```
The API will be available at `http://localhost:8000` (interactive docs at `http://localhost:8000/docs`).

---

## Logging & Audits
Structured application logs are captured asynchronously inside `agentverse_backend/logs/agentverse.log` using `loguru`.
* Logs are rotated **daily at midnight (`00:00`)**.
* Keep-alive history limit is configured to exactly **2 days**, automatically purging older logs to maintain clean local storage.

---

## Core API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/v1/chat/query` | Main endpoint — runs the full LangGraph multi-agent pipeline |
| GET | `/api/v1/health` | Liveness check |

---

## Roadmap

- [x] Modular database schemas (PostgreSQL)
- [x] Dynamic database-driven agent registries
- [x] Alembic migration setup
- [x] Structured logger with daily log-retention
- [ ] Core multi-agent orchestration (LangGraph)
- [ ] RAG pipeline over personal documents
- [ ] Live portfolio + news integration
- [ ] Streamlit dashboard (charts, chat, advisory panel)
- [ ] Docker Compose one-command startup

---

## Status

Actively in development. Currently implementing the core LangGraph skeleton and mock tools in Phase 0.

---

## Author

**Vidur Diwate**
