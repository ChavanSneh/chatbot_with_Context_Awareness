import streamlit as st
import os
from groq import Groq
import openai

# --- 1. SETUP & PAGE CONFIG ---
st.set_page_config(page_title="The Lightning Squad", page_icon="⚡")

# Custom CSS to make it look sharp
st.markdown("""
    <style>
    .main { text-align: center; }
    .stChatInput { margin-top: 20px; }
    </style>
    """, unsafe_allow_html=True)

st.title("⚡ The Lightning Squad")
st.subheader("High-Speed Research & Creative Writing 🤖")

# --- 2. SECRETS LOADING ---
# This pulls from .streamlit/secrets.toml
GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
OPENROUTER_API_KEY = st.secrets["OPENROUTER_API_KEY"]

# --- 3. THE SQUAD BRAINS (Prompts) ---
RESEARCHER_IDENTITY = "You are the Researcher. Find facts and deep context on this topic."
WRITER_IDENTITY = "You are the Expert Writer. Use the Researcher's data to write a punchy, witty, and helpful response."

# --- 4. CHAT HISTORY INITIALIZATION ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display existing chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 5. THE MAIN CHAT INPUT (Only one!) ---
if prompt := st.chat_input("What should the 🏗️ Hybrid Squad investigate?"):
    
    # Add user message to UI
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # --- PHASE 1: THE RESEARCHER (via OpenRouter/Gemini) ---
    with st.status("Researcher is gathering data...", expanded=False) as status:
        client_or = openai.OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=OPENROUTER_API_KEY,
        )
        
        res_response = client_or.chat.completions.create(
            model="google/gemini-2.0-flash-001",
            messages=[
                {"role": "system", "content": RESEARCHER_IDENTITY},
                {"role": "user", "content": prompt}
            ]
        )
        research_data = res_response.choices[0].message.content
        status.update(label="Research complete!", state="complete")

    # --- PHASE 2: THE WRITER (via Groq/Llama) ---
    with st.chat_message("assistant"):
        st.write("Writer is preparing the response...")
        
        client_groq = Groq(api_key=GROQ_API_KEY)
        
        # We pass the research data to the writer so they have context!
        writer_response = client_groq.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": WRITER_IDENTITY},
                {"role": "user", "content": f"Research Data: {research_data}\n\nUser Question: {prompt}"}
            ]
        )
        
        final_answer = writer_response.choices[0].message.content
        st.markdown(final_answer)

    # Save the assistant's response
    st.session_state.messages.append({"role": "assistant", "content": final_answer})