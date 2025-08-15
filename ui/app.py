#!/usr/bin/env python3

import streamlit as st
import httpx

st.set_page_config(page_title="Thoughtful Q&A", page_icon="🤖")
st.title("Thoughtful AI – Support Agent (Demo)")

thr = None
score = None
q = st.text_input("Ask about Thoughtful AI’s Agents")
if st.button("Ask") and q:
    try:
        resp = httpx.post("http://localhost:8000/ask", json={"question": q}, timeout=10)
        data = resp.json()
        st.markdown(f"**Answer** ({data.get('source','?')}): {data.get('answer','')}")
        thr = data.get("threshold")
        score = data.get("score")
    except Exception as e:
        st.error(f"Error contacting backend: {e}")

st.divider()
st.write("Tips: Try “What does EVA do?”, “Tell me about agents”, or “How does PHIL work?”")

if thr is not None and score is not None:
    st.markdown(
        f"<span style='font-size: 0.85em; color: gray;'>Min match for KB: {int(thr)}%<br>Match percentage: {int(round(score))}%</span>",
        unsafe_allow_html=True
    )
elif thr is not None:
    st.caption(f"Min match for KB: {int(thr)}%")
elif score is not None:
    st.caption(f"Match percentage: {int(round(score))}%")
