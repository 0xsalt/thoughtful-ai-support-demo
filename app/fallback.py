#!/usr/bin/env python3

import os
from openai import OpenAI

def llm_fallback(user_q: str, kb_text: str):
    """LLM fallback path when KB retrieval is insufficient.

    Inputs:
      - user_q: str user question
      - kb_text: str serialized KB/context text
    Behavior:
      - If no OPENAI_API_KEY is set, returns a canned, honest default.
      - Otherwise, calls OpenAI Chat Completions with a concise, generic prompt.
    Returns:
      - dict: {"source": "fallback", "answer": "..."}
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return {
            "source": "fallback",
            "answer": "It looks like my OpenAI API key is not configured yet. From our knowledge base, agents include EVA, CAM, and PHIL. Would you like details on those?"
        }

    try:
        client = OpenAI(api_key=api_key)
        messages = [
            {
                "role": "system",
                "content": (
                    "You are a concise customer support assistant for Thoughtful AI. "
                    "The KB did not contain a direct match. Provide a generic, helpful response. "
                    "Avoid fabricating specifics. Keep answers brief."
                ),
            },
            {
                "role": "user",
                "content": f"Question: {user_q}\n\n(Optional KB context):\n{kb_text or ''}",
            },
        ]
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            temperature=0.3,
            max_tokens=200,
        )
        text = (resp.choices[0].message.content or "").strip()
        return {
            "source": "fallback",
            "answer": text or "I can help with general questions about Thoughtful AI."
        }
    except Exception:
        # Remain simple and robust if the provider call fails
        return {
            "source": "fallback",
            "answer": "I can help with general questions about Thoughtful AI."
        }
