import streamlit as st
from langchain_groq import ChatGroq
import os

# --- PAGE SETUP ---
st.set_page_config(page_title="AI Squad", page_icon="🤖")
st.title("🤖 AI Research Squad")

# Get API Key from environment
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

# --- AGENT SETUP ---
def get_agents():
    # Researcher: Using the new '8b-instant' model
    researcher = ChatGroq(model="llama-3.1-8b-instant", groq_api_key=GROQ_API_KEY)
    
    # Writer: Using the new '3.3-70b-versatile' model
    writer = ChatGroq(
        model="llama-3.3-70b-versatile", 
        groq_api_key=GROQ_API_KEY, 
        streaming=True
    )
    return researcher, writer

# Your favorite streaming helper!
def stream_parser(stream):
    for chunk in stream:
        yield chunk.content

# --- SESSION STATE ---
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- CHAT INPUT ---
if prompt := st.chat_input("Ask your squad anything..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.status("🔍 Squad is investigating...", expanded=True) as status:
            agent_r, agent_w = get_agents()
            
            # Step 1: Research
            st.write("Researcher is gathering data...")
            facts = agent_r.invoke(prompt).content
            
            st.write("Writer (Versatile) is preparing the response...")
            
            # Step 2: Write with the ChatGPT feeling
            response_stream = agent_w.stream(f"Research: {facts}\n\nUser Question: {prompt}")
            
            # This is exactly the logic you wanted:
            final_response = st.write_stream(stream_parser(response_stream))
            
            status.update(label="✅ Task Complete!", state="complete")

    st.session_state.messages.append({"role": "assistant", "content": final_response})
