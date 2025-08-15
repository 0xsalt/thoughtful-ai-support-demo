#!/usr/bin/env python3

from rapidfuzz import fuzz, process

def normalize(s: str) -> str:
    return "".join(ch.lower() for ch in s if ch.isalnum() or ch.isspace())

def best_match(user_q: str, qa):
    """Return the best KB match for a user question.

    Inputs:
      - user_q: str user question
      - qa: list of dicts with 'question' and 'answer' keys from the KB
    Behavior:
      - Uses RapidFuzz token_set_ratio on a normalized query against KB questions.
    Returns:
      - (best_index, best_score, answer) when a match exists
      - (None, 0.0, None) when no valid index is found
    """
    # qa: list[{"question": "...", "answer": "..."}]
    choices = [q["question"] for q in qa]
    query = normalize(user_q)
    # token_set ratio is forgiving on word order
    res = process.extractOne(query, choices, scorer=fuzz.token_set_ratio, processor=normalize)
    if not res:
        return None, 0.0, None
    match, score, idx = res
    if idx is None:
        return None, 0.0, None
    return idx, float(score), qa[idx]["answer"]

def answer_from_kb(user_q: str, qa, threshold: int = 78):
    idx, score, ans = best_match(user_q, qa)
    if score >= threshold:
        return {"source": "kb", "score": score, "answer": ans}
    return None
