# Thoughtful AI – Customer Support Agent (Demo)

Important Note: 

* This implementation uses Streamlit + FastAPI. 
* This will not run (easily) on Repl.it in its current state because I implemented it as two separate frontend + backend services and Repl.it by default only supports running one service at a time. 

---

A time-boxed Q&A agent that answers questions about Thoughtful AI’s healthcare Agents
from a hardcoded knowledge base, with a graceful LLM fallback when confidence is low.

- Backend: FastAPI (`/ask`, `/healthz`)
- Retrieval: fuzzy token-set match with match % threshold (RapidFuzz)
- Fallback: LLM provider to handle unmatched questions below threshold %
- Front-end: Single page Streamlit, simple & clean UX

## Features
- Knowledge base is authoritative with graceful fallback to LLM based on KB.
- Source field `kb` or `fallback` displayed in the UI for easy debugging.
- Slider on left to change the keyword lookup minimum match percentage. 

## Test example of search threshold match % tuning and how to ensure the app returns the correct answer.
  - Match percentage starts at 78%
  - If you ask "How does PHIL work?" it will match 83% and return the KB answer. 
  - If you ask "What does PHIL do?" it will match 83% to an answer about EVA and return an incorrect KB answer.
  - Change the KB Match Threshold slider to 84%, then click "Update Threshold". It will update the minimum percentage match and now asking "What does PHIL do?" will still match at 83%, which is now below the minimum threshold, and then fallback to LLM lookup which returns the correct answer.

## Configure variables & project defaults
### Setup .gitignore and .env with API key(s)
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
├── .prjroot
├── README.md
├── .replit
├── requirements.txt
└── ui
    └── app.py
```

## LICENSE

* MIT

## Attribution

* Russ Swift
* Agentic coding partner

