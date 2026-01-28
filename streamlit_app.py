import streamlit as st

from langchain_openai import ChatOpenAI


from langchain_groq import ChatGroq
import os

# --- PAGE CONFIG ---
st.set_page_config(page_title="OpenRouter Squad", page_icon="🕵️")
st.title("⚡The Lightning Squad: Gemini & Groq")

# Get API Keys
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")

st.set_page_config(page_title="AI Squad", page_icon="🤖")
st.title("🤖 AI Research Squad")

# Get API Key from environment

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

# --- AGENT SETUP ---
def get_agents():

    # RESEARCHER: Gemini 1.5 Flash (via OpenRouter)
    researcher = ChatOpenAI(
        model="google/gemini-flash-1.5",
        openai_api_key=OPENROUTER_API_KEY,
        base_url="https://openrouter.ai/api/v1",
        default_headers={
            "HTTP-Referer": "http://localhost:3000", # Optional: your app URL
            "X-Title": "AI Squad App",              # Optional: your app name
        }
    )
    
    # WRITER: Groq (Llama 3.3 Versatile)

    # Researcher: Using the new '8b-instant' model
    researcher = ChatGroq(model="llama-3.1-8b-instant", groq_api_key=GROQ_API_KEY)
    
    # Writer: Using the new '3.3-70b-versatile' model

    writer = ChatGroq(
        model="llama-3.3-70b-versatile", 
        groq_api_key=GROQ_API_KEY, 
        streaming=True
    )
    return researcher, writer


# Your favorite streaming helper

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
if prompt := st.chat_input("What should the squad investigate?"):

if prompt := st.chat_input("Ask your squad anything..."):

    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):

        with st.status("🏗️ Hybrid Squad Processing...", expanded=True) as status:
            agent_r, agent_w = get_agents()
            
            # Step 1: Gemini (OpenRouter) Research
            st.write("🛰️ Gemini is scanning for facts...")
            facts = agent_r.invoke(prompt).content
            
            st.write("✍️ Groq (Versatile) is drafting the report...")
            
            # Step 2: Groq Writing (Streaming)
            response_stream = agent_w.stream(f"Research: {facts}\n\nQuestion: {prompt}")
            
            # This is the "ChatGPT feeling" you wanted:

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

    st.session_state.messages.append({"role": "assistant", "content": final_response})

