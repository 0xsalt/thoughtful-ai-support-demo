#!/usr/bin/env python3

import json, os
from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel
from app.retrieval import best_match
from .fallback import llm_fallback

# Load environment variables from .env file
load_dotenv()

with open(os.path.join(os.path.dirname(__file__), "kb.json"), "r") as f:
    KB = json.load(f)["questions"]
KB_TEXT = json.dumps(KB, indent=2)

class AskReq(BaseModel):
    question: str

class ConfigUpdate(BaseModel):
    threshold: int

app = FastAPI()

@app.get("/healthz")
def healthz():
    return {"ok": True}

@app.get("/config")
def get_config():
    """Get current configuration settings."""
    return {"threshold": int(os.getenv("RETRIEVAL_THRESHOLD", "78"))}

@app.post("/config")
def update_config(config: ConfigUpdate):
    """Update configuration settings and persist to .env file."""
    import re
    
    # Validate threshold range
    if not 0 <= config.threshold <= 100:
        return {"error": "Threshold must be between 0 and 100"}
    
    # Update .env file
    env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
    
    try:
        # Read current .env file
        with open(env_path, 'r') as f:
            lines = f.readlines()
        
        # Update or add RETRIEVAL_THRESHOLD line
        threshold_updated = False
        for i, line in enumerate(lines):
            if line.startswith("RETRIEVAL_THRESHOLD="):
                lines[i] = f"RETRIEVAL_THRESHOLD={config.threshold}\n"
                threshold_updated = True
                break
        
        if not threshold_updated:
            lines.append(f"RETRIEVAL_THRESHOLD={config.threshold}\n")
        
        # Write back to .env file
        with open(env_path, 'w') as f:
            f.writelines(lines)
        
        # Reload environment variables
        load_dotenv(override=True)
        
        return {"threshold": config.threshold, "message": "Configuration updated successfully"}
    
    except Exception as e:
        return {"error": f"Failed to update configuration: {str(e)}"}

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
