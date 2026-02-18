import streamlit as st
import requests

API_URL = "http://localhost:8000"

def render_sidebar(user_id: int):
    with st.sidebar:
        st.title("🎯 AI Career Mentor")
        
        # User Profile Summary
        st.header("Profile")
        user = st.session_state.get("user", {})
        st.write(f"👤 **{user.get('username', 'User')}**")
        st.write(f"📧 {user.get('email', '')}")
        
        if st.button("🚪 Logout", use_container_width=True):
            # Clear all session state
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
        
        st.markdown("---")
        
        # Chat History
        st.header("Chat History")
        
        try:
            response = requests.get(f"{API_URL}/chat/sessions/{user_id}")
            if response.status_code == 200:
                sessions = response.json()
                for session in sessions:
                    session_num = session.get('session_number', session['id'])
                    summary = session.get('summary', 'No Summary')
                    # Truncate summary for display
                    display_summary = summary[:25] + '...' if summary and len(summary) > 25 else summary
                    if st.sidebar.button(
                        f"Session {session_num} - {display_summary}",
                        key=f"session_{session['id']}"
                    ):
                        st.session_state.current_session_id = session['id']
                        st.session_state.messages = []
                        st.session_state.last_loaded_session = None
                        st.rerun()
                
                # Show session count
                st.caption(f"{len(sessions)} / 10 sessions used")
            else:
                st.error("Failed to load history")
        except Exception as e:
            st.error(f"Backend Error: {e}")
            
        if st.sidebar.button("➕ New Chat"):
            st.session_state.current_session_id = None
            st.session_state.messages = []
            st.session_state.last_loaded_session = None
            st.rerun()

        st.markdown("---")
        st.header("Resume Upload")
        uploaded_file = st.file_uploader("Upload your resume", type=["pdf", "txt", "csv", "jpg", "png"])
        if uploaded_file is not None:
            if st.button("📄 Analyze Resume"):
                with st.spinner("Analyzing..."):
                    current_session_id = st.session_state.get("current_session_id")
                    try:
                        url = f"{API_URL}/resumes/upload/{user_id}"
                        if current_session_id:
                            url += f"?session_id={current_session_id}"
                            
                        res = requests.post(url, files={"file": (uploaded_file.name, uploaded_file.getvalue())})
                        if res.status_code == 200:
                            st.success("Resume uploaded and analyzed!")
                        else:
                            st.error("Failed to upload resume.")
                    except Exception as e:
                        st.error(f"Error: {e}")

