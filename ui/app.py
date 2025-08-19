#!/usr/bin/env python3

import streamlit as st
import httpx

st.set_page_config(page_title="Thoughtful Q&A", page_icon="🤖", layout="wide")
st.title("Thoughtful AI – Support Agent (Demo)")

# Configuration sidebar
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # Get current threshold
    try:
        config_resp = httpx.get("http://localhost:8000/config", timeout=5)
        if config_resp.status_code == 200:
            current_threshold = config_resp.json().get("threshold", 78)
        else:
            st.warning("⚠️ Could not fetch current threshold, using default (78%)")
            current_threshold = 78
    except Exception as e:
        st.warning("⚠️ Backend not available, using default threshold (78%)")
        current_threshold = 78
    
    # Threshold slider
    new_threshold = st.slider(
        "KB Match Threshold (%)", 
        min_value=0, 
        max_value=100, 
        value=current_threshold,
        help="Minimum confidence percentage required to use knowledge base instead of LLM fallback"
    )
    
    # Update button
    if st.button("🔄 Update Threshold"):
        try:
            update_resp = httpx.post(
                "http://localhost:8000/config", 
                json={"threshold": new_threshold}, 
                timeout=5
            )
            if update_resp.status_code == 200:
                st.success("✅ Threshold updated successfully!")
                st.rerun()
            else:
                st.error(f"❌ Failed to update: {update_resp.json().get('error', 'Unknown error')}")
        except Exception as e:
            st.error(f"❌ Error updating threshold: {e}")
    
    st.divider()
    st.caption(f"Current threshold: {current_threshold}%")

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
