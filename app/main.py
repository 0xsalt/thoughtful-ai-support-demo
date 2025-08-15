#!/usr/bin/env python3

import json, os
from fastapi import FastAPI
from pydantic import BaseModel
from app.retrieval import best_match
from .fallback import llm_fallback

with open(os.path.join(os.path.dirname(__file__), "kb.json"), "r") as f:
    KB = json.load(f)["questions"]
KB_TEXT = json.dumps(KB, indent=2)

class AskReq(BaseModel):
    question: str

app = FastAPI()

@app.get("/healthz")
def healthz():
    return {"ok": True}

@app.post("/ask")
def ask(req: AskReq):
    """Q&A endpoint that prefers KB retrieval and falls back to an LLM.

    Purpose:
      - Tries knowledge-base retrieval first; if confidence is below threshold, uses LLM fallback.

    Inputs:
      - request body: {"question": str}

    Returns:
      - JSON dict with:
        - "answer": str
        - "source": "kb" or "fallback"
        - always includes "score" (float 0–100) and "threshold" (int)
    """
    THRESHOLD = int(os.getenv("RETRIEVAL_THRESHOLD", "78"))
    idx, score, ans = best_match(req.question, KB)
    if score >= THRESHOLD:
        return {"source": "kb", "answer": ans, "score": score, "threshold": THRESHOLD}
    else:
        fb = llm_fallback(req.question, KB_TEXT)
        return {**fb, "score": score, "threshold": THRESHOLD}
