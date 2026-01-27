import streamlit as st
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="AI Squad Hub (Groq Powered)", 
    page_icon="⚡", 
    layout="centered"
)

# Custom CSS for modern chat bubbles
st.markdown("""
    <style>
    .stChatMessage { border-radius: 15px; margin-bottom: 10px; }
    .stChatInputContainer { padding-bottom: 20px; }
    </style>
""", unsafe_allow_html=True)

# --- 2. SETUP & SECURITY ---
load_dotenv()
# We use GROQ_API_KEY from your .env file
groq_api_key = os.getenv("GROQ_API_KEY")

# Stop the app if the key is missing
if not groq_api_key:
    st.error("❌ GROQ_API_KEY not found in .env file!")
    st.stop()

# Initialize the Agents (Llama 3.3 70B is the 'Ferrari' of free models right now)
researcher = ChatGroq(
    model_name="llama-3.3-70b-versatile",
    api_key=groq_api_key,
    temperature=0.1
)

writer = ChatGroq(
    model_name="llama-3.3-70b-versatile",
    api_key=groq_api_key,
    temperature=0.7
)

# --- 3. SIDEBAR SETTINGS ---
with st.sidebar:
    st.title("⚡ Groq Squad Settings")
    st.markdown("---")
    st.success("Connected to Groq LPU™")
    st.info("**Researcher:** Llama 3.3 70B\n\n**Writer:** Llama 3.3 70B")
    
    if st.button("Clear Chat History"):
        st.session_state.chat_history = []
        st.rerun()

# --- 4. CHAT HISTORY LOGIC ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Display previous messages from session memory
for message in st.session_state.chat_history:
    role = "user" if isinstance(message, HumanMessage) else "assistant"
    with st.chat_message(role):
        st.markdown(message.content)

# --- 5. CHAT INPUT & SQUAD LOGIC ---
if user_query := st.chat_input("Ask your Groq Squad..."):
    # Display user message instantly
    with st.chat_message("user"):
        st.markdown(user_query)
    st.session_state.chat_history.append(HumanMessage(content=user_query))

    # AI Process: Showing the 'Thinking' steps
    with st.chat_message("assistant"):
        with st.status("🚀 Squad is sprinting...", expanded=True) as status:
            # Step 1: Research
            st.write("🔍 Researcher is analyzing data...")
            research_query = f"Provide detailed facts and context for: {user_query}"
            facts = researcher.invoke(research_query).content
            
            # Step 2: Write
            st.write("✍️ Writer is crafting the response...")
            writing_prompt = f"Using these facts: {facts}, write a helpful response to: {user_query}"
            final_response = writer.invoke(writing_prompt).content
            
            status.update(label="✅ Task Complete!", state="complete", expanded=False)
        
        # Display Final Result
        st.markdown(final_response)
        st.session_state.chat_history.append(AIMessage(content=final_response))