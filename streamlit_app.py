import streamlit as st
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(page_title="AI Squad Hub", page_icon="🤖", layout="centered")

# Custom CSS for a cleaner look
st.markdown("""
    <style>
    .stChatMessage { border-radius: 15px; margin-bottom: 10px; }
    .stChatInputContainer { padding-bottom: 20px; }
    </style>
""", unsafe_allow_html=True)

# --- 2. SETUP & SECURITY ---
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

# Check if API key exists
if not api_key:
    st.error("❌ GOOGLE_API_KEY not found! Please check your .env file.")
    st.stop()

# Initialize the Agents
from langchain_groq import ChatGroq  # 👈 Make sure this is in your imports!

# Setup the Squad with Groq (Llama 3.3 70B)
# High speed + High intelligence = Best for Agents
researcher = ChatGroq(
    model_name="llama-3.3-70b-versatile",
    groq_api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.1
)

writer = ChatGroq(
    model_name="llama-3.3-70b-versatile",
    groq_api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.7
)

# --- 3. SIDEBAR SETTINGS ---
with st.sidebar:
    st.title("🤖 AI Squad Settings")
    st.markdown("---")
    st.info("**Researcher:** Gathers facts\n\n**Writer:** Polishes the final response")
    if st.button("Clear Chat History"):
        st.session_state.chat_history = []
        st.rerun()

# --- 4. CHAT HISTORY LOGIC ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Display previous messages
for message in st.session_state.chat_history:
    role = "user" if isinstance(message, HumanMessage) else "assistant"
    with st.chat_message(role):
        st.markdown(message.content)

# --- 5. CHAT INPUT & SQUAD LOGIC ---
if user_query := st.chat_input("What should the squad work on?"):
    # Display user message
    with st.chat_message("user"):
        st.markdown(user_query)
    st.session_state.chat_history.append(HumanMessage(content=user_query))

    # AI Process
    with st.chat_message("assistant"):
        with st.status("🛠️ Squad at work...", expanded=True) as status:
            # Step 1: Research
            st.write("🔍 Researcher is gathering data...")
            research_query = f"Provide detailed facts and context for: {user_query}"
            facts = researcher.invoke(research_query).content
            
            # Step 2: Write
            st.write("✍️ Writer is crafting the response...")
            writing_prompt = f"Using these facts: {facts}, write a helpful response to the user's request: {user_query}"
            final_response = writer.invoke(writing_prompt).content
            
            status.update(label="✅ Task Complete!", state="complete", expanded=False)
        
        # Display Final Result
        st.markdown(final_response)
        st.session_state.chat_history.append(AIMessage(content=final_response))