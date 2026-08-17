# AgentVerse

**AI-Powered Financial Portfolio Advisor** — a multi-agent system built with LangGraph, FastAPI, and RAG.

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
| LLM (reasoning) | OpenAI API |
| Embeddings | Hugging Face sentence-transformers (local) |
| Vector Database | ChromaDB (local, persistent) |
| Relational Database | PostgreSQL + SQLAlchemy ORM |
| Live Stock Data | Finnhub API |
| Live News Data | NewsAPI.org |
| Caching | cachetools (in-memory TTL cache) |

---

## Project Structure

```
agentverse/
├── backend/
│   ├── main.py                 # FastAPI app entrypoint
│   ├── config.py                # env vars, API keys, constants
│   ├── api/                     # route handlers
│   ├── agents/                  # LangGraph graph + agent nodes
│   ├── tools/                   # external API wrappers + caching
│   ├── db/                      # SQLAlchemy models, session, CRUD
│   ├── schemas/                 # Pydantic models
│   ├── memory/                  # short-term memory logic
│   ├── vectorstore/             # ChromaDB client + ingestion
│   └── requirements.txt
├── frontend/
│   ├── app.py                   # Streamlit entrypoint
│   ├── components/               # chat, charts, news, advisory panels
│   └── requirements.txt
├── data/
│   └── chroma_store/             # ChromaDB persistent storage
├── docker-compose.yml            # PostgreSQL + backend + frontend
├── .env.example
└── README.md
```

---

## Getting Started

### Prerequisites
- Python 3.10+
- PostgreSQL (local install or via Docker)
- API keys: OpenAI, Finnhub, NewsAPI.org (all have free tiers)

### 1. Clone and set up environment variables
```bash
git clone <repo-url>
cd agentverse
cp .env.example .env
# fill in: DATABASE_URL, OPENAI_API_KEY, FINNHUB_API_KEY, NEWSAPI_KEY
```

### 2. Backend setup
```bash
cd backend
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Run DB migrations / create tables
python -m db.init_db

uvicorn main:app --reload --port 8000
```

### 3. Frontend setup
```bash
cd frontend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

streamlit run app.py
```

### 4. (Optional) Run everything with Docker
```bash
docker-compose up --build
```

The API will be available at `http://localhost:8000` (docs at `/docs`) and the dashboard at `http://localhost:8501`.

---

## Core API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/v1/chat/{session_id}/query` | Main endpoint — runs the full LangGraph multi-agent pipeline |
| GET | `/api/v1/portfolio/{user_id}/performance` | Live portfolio performance |
| POST | `/api/v1/documents/{user_id}/upload` | Upload a financial document for RAG |
| GET | `/api/v1/health` | Liveness check |

Full endpoint list, request/response schemas, and database schema are documented in `AgentVerse_LLD_Document.pdf`.

---

## Roadmap

- [x] Core multi-agent orchestration (LangGraph)
- [x] RAG pipeline over personal documents
- [x] Live portfolio + news integration
- [x] Short-term conversational memory
- [ ] Streamlit dashboard (charts, chat, advisory panel)
- [ ] Docker Compose one-command startup
- [ ] Evaluation suite for retrieval accuracy and agent routing

---

## Status

Actively in development. Currently built and tested as a local, single-user system with production-grade architecture patterns (async APIs, structured state, caching, persistent memory).

---

## Author

**Vidur Diwate**
