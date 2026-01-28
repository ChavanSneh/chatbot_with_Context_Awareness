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
    # Researcher stays fast and direct
    researcher = ChatGroq(model="llama3-8b-8192", groq_api_key=GROQ_API_KEY)
    # Writer uses the big model with streaming enabled for the "ChatGPT feeling"
    writer = ChatGroq(model="llama3-70b-8192", groq_api_key=GROQ_API_KEY, streaming=True)
    return researcher, writer

# Helper function to handle the stream chunks
def stream_parser(stream):
    for chunk in stream:
        yield chunk.content

# --- SESSION STATE ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display old messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- CHAT INPUT ---
if prompt := st.chat_input("Ask your squad anything..."):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Assistant Response
    with st.chat_message("assistant"):
        with st.status("🔍 Squad is investigating...", expanded=True) as status:
            agent_r, agent_w = get_agents()
            
            # 1. Researcher finds facts (Static)
            st.write("Researcher is gathering data...")
            facts = agent_r.invoke(prompt).content
            
            st.write("Writer is preparing the response...")
            
            # 2. Writer streams the response (The ChatGPT feeling!)
            response_stream = agent_w.stream(f"Research: {facts}\n\nUser Question: {prompt}")
            
            # This line animates the text as it comes in
            final_response = st.write_stream(stream_parser(response_stream))
            
            status.update(label="✅ Task Complete!", state="complete")

    # Save the full final response to history
    st.session_state.messages.append({"role": "assistant", "content": final_response})
