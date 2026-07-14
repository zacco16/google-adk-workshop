# Travel Planner AI

A travel planning agent built with **Google ADK** + **Gemini**, served through **FastAPI** with a lightweight HTML chat frontend. Ask about a destination and the agent recommends attractions, seasonal highlights, and local events — with conversation memory across turns.

> Building on the workshop starter kit — see [`README-ws.md`](./README-ws.md) for the original workshop instructions and TODO walkthrough.

---

## Stack

| Layer | Technology |
|---|---|
| Agent framework | [Google ADK](https://google.github.io/adk-docs/) |
| LLM | Gemini 2.5 Flash |
| API server | FastAPI + Uvicorn |
| Frontend | Single-page vanilla-JS chat UI (served by FastAPI at `/`) |
| Dependency management | [uv](https://docs.astral.sh/uv/) |

---

## Quick Start

### 1. Install dependencies

```bash
uv sync
```

This creates a `.venv` and installs everything from `pyproject.toml`.

### 2. Configure your API key

Copy the example env file and add your Gemini key:

```bash
cp my_travel_planner/.env.example my_travel_planner/.env
```

Then edit `my_travel_planner/.env` and set:

```env
GEMINI_API_KEY=your_gemini_api_key_here
```

> Get a key from [Google AI Studio](https://aistudio.google.com/app/apikey). The `.env` file is gitignored — never commit it.

### 3. Boot the app (with the HTML frontend)

```bash
uv run uvicorn api:app --reload --port 8002
```

Then open the chat UI in your browser:

**http://localhost:8002/**

Type a destination (e.g. *"Best things to do in Paris in spring?"*), hit **Send**, and the agent replies inline. Because memory is retained server-side, you can ask follow-ups like *"what about in winter?"* and it keeps the context.

> `--reload` auto-restarts on code changes (which also clears the in-memory conversation). Any free port works — just match it in the URL.

---

## Other Endpoints

The same server also exposes:

| URL | What it is |
|---|---|
| `http://localhost:8002/` | HTML chat frontend |
| `http://localhost:8002/ask` | Agent API (POST JSON) |
| `http://localhost:8002/docs` | Swagger UI |

**Query the API directly:**

```bash
curl -X POST http://localhost:8002/ask \
  -H "Content-Type: application/json" \
  -d '{"query": "Best things to do in Paris in spring?"}'
```

Response:

```json
{
  "query": "Best things to do in Paris in spring?",
  "response": "Paris in spring is magical! ..."
}
```

---

## Run Without the Server (CLI)

Run the agent once from the terminal (fires a sample query and prints the answer):

```bash
uv run python run.py
```

---

## Project Structure

```
google-adk-workshop/
├── my_travel_planner/
│   ├── agent.py          # Root agent definition (get_root_agent)
│   ├── .env.example      # Env template — copy to .env
│   └── .env              # Your API key (gitignored)
├── static/
│   └── index.html        # HTML chat frontend
├── run.py                # Session/runner wiring + response streaming
├── api.py                # FastAPI app: serves frontend (/) and agent API (/ask)
└── pyproject.toml        # Project dependencies
```

---

## Notes

- **Conversation memory** is in-memory and shared across all clients via a single session; it resets whenever the server restarts. See `run.py` for where the session service is created.
- **No CORS setup** is needed — the frontend is served by the same FastAPI app, so it's same-origin with `/ask`.
