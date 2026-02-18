import streamlit as st
import requests

API_URL = "http://localhost:8000"

def render_chat(user_id: int):
    st.header("💬 Chat with your Mentor")
    
    current_session = st.session_state.get("current_session_id", None)
    
    # Initialize chat history or fetch from backend
    if "messages" not in st.session_state or st.session_state.get("last_loaded_session") != current_session:
        st.session_state.messages = []
        st.session_state.last_loaded_session = current_session
        
        if current_session:
            try:
                res = requests.get(f"{API_URL}/chat/history/{current_session}")
                if res.status_code == 200:
                    history = res.json()
                    for msg in history:
                        st.session_state.messages.append({"role": msg["role"], "content": msg["content"]})
            except Exception as e:
                st.error(f"Failed to load chat history: {e}")
        
    # Input at the top
    with st.form(key="chat_form", clear_on_submit=True):
        col1, col2 = st.columns([6, 1])
        with col1:
            prompt = st.text_input("Ask about your career path...", key="chat_input_field", label_visibility="collapsed", placeholder="Ask about your career path...")
        with col2:
            submit_button = st.form_submit_button("Send")
            
    if submit_button and prompt:
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        session_id = st.session_state.get("current_session_id")
        
        # Create new session if none exists
        if not session_id:
            try:
                session_payload = {"user_id": user_id, "summary": prompt[:30] + "..."}
                res = requests.post(f"{API_URL}/chat/sessions/", json=session_payload)
                if res.status_code == 200:
                    new_session = res.json()
                    session_id = new_session["id"]
                    st.session_state.current_session_id = session_id
                else:
                    st.error("Failed to create new session")
                    st.stop()
            except Exception as e:
                st.error(f"Error creating session: {e}")
                st.stop()

        # Send to API
        payload = {
            "session_id": session_id,
            "user_id": user_id,
            "role": "user",
            "content": prompt
        }
        
        try:
            with st.spinner("Thinking..."):
                response = requests.post(f"{API_URL}/chat/messages/", json=payload)
                if response.status_code == 200:
                    ai_message = response.json()
                    response_text = ai_message.get("content", "Error: No response content")
                else:
                    response_text = "Error: Failed to get response from server."
        except Exception as e:
            response_text = f"Error: {e}"

        st.session_state.messages.append({"role": "assistant", "content": response_text})
        st.rerun()

    # Display chat messages from history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
