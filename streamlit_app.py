import streamlit as st
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage

# 1. Setup & Security
load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")
or_url = "https://openrouter.ai/api/v1"

# Page Config
st.set_page_config(page_title="The AI Squad", layout="wide")
st.title("🤖 The AI Squad: Context-Aware Chat")

# 2. Initialize the Agents (The Squad)
# Note the commas and max_tokens=500 to keep within credit limits
researcher = ChatOpenAI(
    model="google/gemini-flash-1.5-exp:free",
    openai_api_key=api_key,
    openai_api_base=or_url,
    max_tokens=500,
)

writer = ChatOpenAI(
    model="google/gemini-flash-1.5-exp:free",
    openai_api_key=api_key,
    openai_api_base=or_url,
    max_tokens=500,
)

# 3. Initialize Memory (Context Awareness)
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Display previous chat messages
for message in st.session_state.chat_history:
    if isinstance(message, HumanMessage):
        with st.chat_message("user"):
            st.markdown(message.content)
    elif isinstance(message, AIMessage):
        with st.chat_message("assistant"):
            st.markdown(message.content)

# 4. Chat Logic
if user_input := st.chat_input("Ask your squad anything..."):
    # Show user message
    with st.chat_message("user"):
        st.markdown(user_input)
    
    # Add to history
    st.session_state.chat_history.append(HumanMessage(content=user_input))

    with st.chat_message("assistant"):
        with st.spinner("The Squad is thinking..."):
            # Prepare context for the agents
            context = st.session_state.chat_history[-5:] # Last 5 messages for memory

            # Agent 1: Researcher (Gathers facts)
            research_query = [
                SystemMessage(content="You are the Researcher. Find key facts and details."),
                *context
            ]
            raw_facts = researcher.invoke(research_query).content

            # Agent 2: Writer (Polishes the answer)
            writing_query = [
                SystemMessage(content=f"You are the Writer. Use these facts: {raw_facts}. Be concise."),
                *context
            ]
            final_answer = writer.invoke(writing_query).content

            # Show the final result
            st.markdown(final_answer)
            
            # Add final answer to memory
            st.session_state.chat_history.append(AIMessage(content=final_answer))

# Sidebar Info
with st.sidebar:
    st.info("The Researcher finds the facts, and the Writer polishes the answer. Your conversation is remembered!")
    if st.button("Clear Chat Memory"):
        st.session_state.chat_history = []
        st.rerun()