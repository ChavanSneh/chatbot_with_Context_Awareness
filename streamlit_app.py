import streamlit as st
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

# Load your OpenRouter Key from .env
load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY") # Make sure this matches your .env file!
or_url = "https://openrouter.ai/api/v1"

st.set_page_config(page_title="Multi-Agent Chat", page_icon="🤖")
st.title("The AI Squad 🤖🤖")

# 1. Initialize Memory (The Shared State)
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        SystemMessage(content="You are a collaborative AI team.")
    ]

# 2. Define your Agents (The Specialists)
# Agent 1: Fast & Logical (Llama 3)
researcher = ChatOpenAI(
    model="meta-llama/llama-3-8b-instruct",
    openai_api_key=api_key,
    openai_api_base=or_url
)

# Agent 2: Creative & Sophisticated (Claude 3.5 or GPT-4o)
writer = ChatOpenAI(
    model="anthropic/claude-3.5-sonnet", 
    openai_api_key=api_key,
    openai_api_base=or_url
)

# 3. Display Chat
for message in st.session_state.chat_history:
    if isinstance(message, (HumanMessage, AIMessage)):
        role = "user" if isinstance(message, HumanMessage) else "assistant"
        with st.chat_message(role):
            st.markdown(message.content)

# 4. The Multi-Agent Workflow
if user_query := st.chat_input("Ask your team..."):
    st.session_state.chat_history.append(HumanMessage(content=user_query))
    with st.chat_message("user"):
        st.markdown(user_query)

    with st.chat_message("assistant"):
        # Step A: Researcher Agent thinks first
        with st.status("Researcher is thinking...", expanded=False):
            # Pass full history for Context Awareness
            research_notes = researcher.invoke(st.session_state.chat_history)
            st.write("Done researching.")

        # Step B: Writer Agent polishes the research
        with st.status("Writer is crafting response...", expanded=False):
            # We give the writer the research notes + history
            final_response = writer.invoke(
                st.session_state.chat_history + [AIMessage(content=f"Notes: {research_notes.content}")]
            )
        
        st.markdown(final_response.content)
        st.session_state.chat_history.append(AIMessage(content=final_response.content))
