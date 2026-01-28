# ⚡ The Lightning Squad: Hybrid AI Chatbot

A high-speed, dual-engine chatbot built with **Streamlit**, **Groq**, and **OpenRouter (Gemini)**. This app uses a "Research & Write" pipeline to deliver fast, fact-based, and creative responses.

## 🚀 The Architecture
The Lightning Squad operates using two distinct AI "Agents":
1. **The Researcher (Google Gemini 3 Flash):** Scans for facts, context, and data.
2. **The Writer (Meta Llama 3.3 70B):** Takes the research and crafts a punchy, tactical response.



## ✨ Features
- **Dual-Model Processing:** Combines Gemini's reasoning with Groq's Llama-3 speed.
- **Context Awareness:** The writer knows what the researcher found.
- **Modern UI:** A clean, dark-themed interface.
- **Tactical Persona:** Specialized system prompts for a unique identity.

## 🛠️ Setup & Installation

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/ChavanSneh/chatbot_with_Context_Awareness.git](https://github.com/ChavanSneh/chatbot_with_Context_Awareness.git)
   cd chatbot_with_Context_Awareness

2. **Install Dependencies**
   pip install -r requirements.txt

3. **Configure Secrets**
   GROQ_API_KEY = "your_groq_key_here"
   OPENROUTER_API_KEY = "your_openrouter_key_here"

4. **Run the App**
   streamlit run streamlit_app.py

🧠 **Technologies Used**
    1)Streamlit: For the fortend dashboard
    2)Groq Cloud: For ultra-low latency interface.
    3)OpenRouter: To access Gemini 2.0 Flash.
    4)Python: The backbone of the logic.
    Developed by Sneh Chavan and Gemini 3 Flash - "Strike fast, Strike Precise." ⚡