import streamlit as st
import os
from dotenv import load_dotenv

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="AI Squad Hub (Groq Powered)", 
    page_icon="⚡", 
    layout="centered"
)

# Custom CSS for a cleaner UI
st.markdown("""
    <style>
    .stChatMessage { border-radius: 15px; margin-bottom: 10px; }
    .stChatInputContainer { padding-bottom: 20px; }
    </style>
""", unsafe_allow_html=True)

# --- 2. SETUP & SECURITY ---
load_dotenv()
# Check for key in .env or system environment
api_key = os.getenv("GROQ_API_KEY")

def initialize_squad():
    """Initializes agents inside a function to prevent circular import errors."""
    try:
        from langchain_groq import ChatGroq
        
        # Researcher: Low temperature for factual accuracy
        researcher_bot = ChatGroq(
            model_name="llama-3.3-70b-versatile",
            api_key=api_key,
            temperature=0.1
        )
        
        # Writer: Higher temperature for natural, creative flow
        writer_bot = ChatGroq(
            model_name="llama-3.3-70b-versatile",
            api_key=api_key,
            temperature=0.7
        )
        return researcher_bot, writer_bot
    except Exception as e:
        st.error(f"Failed to load AI Agents: {e}")
        return None, None

# --- 3. SIDEBAR ---
with st.sidebar:
    st.title("⚡ Groq Squad Settings")
    st.markdown("---")
    if not api_key:
        st.error("❌ GROQ_API_KEY is missing!")
        st.info("Please add it to your .env file like this:\nGROQ_API_KEY=gsk_...")
    else:
        st.success("Connected to Groq LPU™")
    
    if st.button("Clear Chat History"):
        st.session_state.chat_history = []
        st.rerun()

# --- 4. CHAT HISTORY LOGIC ---
from langchain_core.messages import HumanMessage, AIMessage

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

for message in st.session_state.chat_history:
    role = "user" if isinstance(message, HumanMessage) else "assistant"
    with st.chat_message(role):
        st.markdown(message.content)

# --- 5. MAIN CHAT INPUT ---
if user_query := st.chat_input("What should the squad work on?"):
    if not api_key:
        st.warning("Please provide an API Key in the .env file first.")
    else:
        # Display user message
        with st.chat_message("user"):
            st.markdown(user_query)
        st.session_state.chat_history.append(HumanMessage(content=user_query))

        # Get the agents
        researcher, writer = initialize_squad()

        if researcher and writer:
            with st.chat_message("assistant"):
                with st.status("🤖 Squad is working...", expanded=True) as status:
                    # Step 1: Research
                    st.write("🔍 Researcher is searching...")
                    res_query = f"Provide detailed facts and context for: {user_query}"
                    facts = researcher.invoke(res_query).content
                    
                    # Step 2: Write
                    st.write("✍️ Writer is crafting...")
                    writing_prompt = f"Using these facts: {facts}, write a helpful response to: {user_query}"
                    final_response = writer.invoke(writing_prompt).content
                    
                    status.update(label="✅ Task Complete!", state="complete")
                
                # Display Result
                st.session_state.chat_history.append(AIMessage(content=final_response))