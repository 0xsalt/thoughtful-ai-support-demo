# Thoughtful AI – Customer Support Agent (Demo)

A time-boxed Q&A agent that answers questions about Thoughtful AI’s healthcare Agents
from a hardcoded knowledge base, with a graceful LLM fallback when confidence is low.

- Backend: FastAPI (`/ask`, `/healthz`)
- Retrieval: fuzzy token-set match with match % threshold (RapidFuzz)
- Fallback: LLM provider to handle unmatched questions below threshold %
- Front-end: Single page Streamlit, simple & clean UX

## Why this design
- 20-30 minutes time-boxed, minimize deps, maximize clarity.
- Reliability: knowledge base is authoritative with graceful fallback to LLM based on KB.
- Observability: Source field `kb` or `fallback` displayed in the UI for easy debugging.

## Configure variables & project defaults
### Configure .gitignore and .env with API key(s)
```
echo -e ".env\n.venv" >> .gitignore  
cp .env.example .env # and fill in your API key(s)  
```

## Run

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
# new shell:
streamlit run ui/app.py
````

## Tests / Health

* `GET /healthz` returns `{"ok": true}`
  * Example: curl <url>:[port]/healthz
* KB retrieval threshold tuned to avoid weak matches.

## Known Limitations / Future Roadmap Opportunities

* Small JSON KB. Matching can be improved using TF‑IDF or embeddings.
  * For example asking "What does PHIL do?" currently returns the info about EVA because RapidFuzz matches more words in the KB entry for EVA.
  * 
* LLM fallback is guardrailed to cite only KB content.

## Repo Structure
```
./
├── app
│   ├── fallback.py
│   ├── kb.json
│   ├── main.py
│   └── retrieval.py
├── docs
│   └── thoughtful-ai-agent.txt
├── .env.example
├── .gitignore
├── .gitignore.example
├── LICENSE
├── README.md
├── requirements.txt
└── ui
    └── app.py
```

## Attribution

* Russ Swift
* Agentic coding partner

