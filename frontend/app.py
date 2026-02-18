import streamlit as st
from components.sidebar import render_sidebar
from components.chat_ui import render_chat
from components.visualizations import render_visualizations
from components.roadmap_ui import render_roadmap
import requests

API_URL = "http://localhost:8000"

st.set_page_config(page_title="AI Career Recommender", layout="wide", initial_sidebar_state="collapsed")

def show_homepage():
    """Show the landing page with project information."""
    
    # Hero Section
    st.markdown("""
    <div style='text-align: center; padding: 2rem 0;'>
        <h1 style='font-size: 3.5rem; margin-bottom: 1rem;'>🎯 AI Career Mentor</h1>
        <p style='font-size: 1.5rem; color: gray; margin-bottom: 2rem;'>
            Your Personal AI-Powered Career Guidance Platform
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Call to action buttons
    col1, col2, col3, col4, col5 = st.columns([1, 1, 0.5, 1, 1])
    with col2:
        if st.button("🔑 Login to Your Account", use_container_width=True, type="primary"):
            st.session_state.auth_page = "login"
            st.rerun()
    with col4:
        if st.button("📝 Create New Account", use_container_width=True):
            st.session_state.auth_page = "register"
            st.rerun()
    
    st.markdown("---")
    
    # Features Section
    st.markdown("## ✨ What We Offer")
    
    feature_col1, feature_col2 = st.columns(2)
    
    with feature_col1:
        st.markdown("""
        ### 💬 **AI Career Chat**
        Chat with GPT-4o-mini powered mentor that remembers your resume and conversation history. Get personalized career advice, skill recommendations, and interview preparation tips.
        
        ### 📊 **Growth Analytics**
        Visualize your skill proficiency with interactive charts. Track your progress over time and identify areas for improvement with AI-driven insights.
        """)
    
    with feature_col2:
        st.markdown("""
        ### 🗺️ **Interactive Career Roadmap**
        Get a personalized step-by-step career roadmap with learning resources, estimated timelines, and difficulty levels. Mark completed steps and track your journey.
        
        ### 📄 **Resume Analysis**
        Upload your resume (PDF, TXT, CSV) and let AI extract your skills, experience level, and education. Get instant career recommendations based on your profile.
        """)
    
    st.markdown("---")
    
    # How It Works Section
    st.markdown("## 🚀 How It Works")
    
    step_col1, step_col2, step_col3, step_col4 = st.columns(4)
    
    with step_col1:
        st.markdown("""
        <div style='text-align: center; padding: 1rem;'>
            <div style='font-size: 3rem;'>1️⃣</div>
            <h4>Create Account</h4>
            <p>Register with your email and create a secure account</p>
        </div>
        """, unsafe_allow_html=True)
    
    with step_col2:
        st.markdown("""
        <div style='text-align: center; padding: 1rem;'>
            <div style='font-size: 3rem;'>2️⃣</div>
            <h4>Upload Resume</h4>
            <p>Upload your resume and let AI analyze your profile</p>
        </div>
        """, unsafe_allow_html=True)
    
    with step_col3:
        st.markdown("""
        <div style='text-align: center; padding: 1rem;'>
            <div style='font-size: 3rem;'>3️⃣</div>
            <h4>Chat & Explore</h4>
            <p>Chat with AI mentor and explore career opportunities</p>
        </div>
        """, unsafe_allow_html=True)
    
    with step_col4:
        st.markdown("""
        <div style='text-align: center; padding: 1rem;'>
            <div style='font-size: 3rem;'>4️⃣</div>
            <h4>Track Progress</h4>
            <p>Follow your personalized roadmap and achieve goals</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Tech Stack Section
    st.markdown("## 🛠️ Built With Modern Technology")
    
    tech_col1, tech_col2, tech_col3 = st.columns(3)
    
    with tech_col1:
        st.markdown("""
        **Backend & AI**
        - FastAPI (Python web framework)
        - OpenAI GPT-4o-mini
        - ChromaDB (Vector database)
        - LangChain (AI orchestration)
        """)
    
    with tech_col2:
        st.markdown("""
        **Frontend & Design**
        - Streamlit (Interactive UI)
        - Plotly (Data visualization)
        - Responsive design
        """)
    
    with tech_col3:
        st.markdown("""
        **Data & Security**
        - PostgreSQL (Database)
        - Bcrypt (Password hashing)
        - SQLAlchemy (ORM)
        """)
    
    st.markdown("---")
    
    # Footer CTA
    st.markdown("""
    <div style='text-align: center; padding: 2rem 0;'>
        <h3>Ready to Accelerate Your Career? 🚀</h3>
        <p style='color: gray;'>Join thousands of professionals using AI to achieve their career goals</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Footer buttons (repeated for convenience)
    col1, col2, col3, col4, col5 = st.columns([1, 1, 0.5, 1, 1])
    with col2:
        if st.button("🔑 Login", use_container_width=True, type="primary", key="footer_login"):
            st.session_state.auth_page = "login"
            st.rerun()
    with col4:
        if st.button("📝 Register", use_container_width=True, key="footer_register"):
            st.session_state.auth_page = "register"
            st.rerun()

def show_login_page():
    """Show dedicated login page."""
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("<h1 style='text-align: center;'>🔑 Login to Your Account</h1>", unsafe_allow_html=True)
        st.markdown("---")
        
        with st.form("login_form"):
            username = st.text_input("Username", placeholder="Enter your username")
            password = st.text_input("Password", type="password", placeholder="Enter your password")
            submit = st.form_submit_button("Login", use_container_width=True, type="primary")
            
            if submit:
                if not username or not password:
                    st.error("Please fill in both fields.")
                else:
                    try:
                        res = requests.post(
                            f"{API_URL}/auth/login",
                            json={"username": username, "password": password}
                        )
                        if res.status_code == 200:
                            user_data = res.json()
                            st.session_state.user = user_data
                            st.session_state.messages = []
                            st.session_state.current_session_id = None
                            st.session_state.auth_page = None
                            st.success(f"Welcome back, {user_data['username']}!")
                            st.rerun()
                        else:
                            error_detail = res.json().get("detail", "Login failed")
                            st.error(error_detail)
                    except Exception as e:
                        st.error(f"Cannot connect to backend: {e}")
        
        st.markdown("---")
        if st.button("⬅️ Back to Home", use_container_width=True):
            st.session_state.auth_page = None
            st.rerun()
        
        st.markdown("<p style='text-align: center; color: gray; margin-top: 1rem;'>Don't have an account? <a href='#' style='color: #ff4b4b;'>Register here</a></p>", unsafe_allow_html=True)
        if st.button("Create New Account", use_container_width=True, key="switch_to_register"):
            st.session_state.auth_page = "register"
            st.rerun()

def show_register_page():
    """Show dedicated register page."""
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("<h1 style='text-align: center;'>📝 Create Your Account</h1>", unsafe_allow_html=True)
        st.markdown("---")
        
        with st.form("register_form"):
            new_username = st.text_input("Username", placeholder="Choose a username")
            new_email = st.text_input("Email", placeholder="Enter your email")
            new_password = st.text_input("Password", type="password", placeholder="Choose a password (min 6 characters)")
            confirm_password = st.text_input("Confirm Password", type="password", placeholder="Confirm your password")
            register_submit = st.form_submit_button("Create Account", use_container_width=True, type="primary")
            
            if register_submit:
                if not new_username or not new_email or not new_password:
                    st.error("Please fill in all fields.")
                elif new_password != confirm_password:
                    st.error("Passwords do not match.")
                elif len(new_password) < 6:
                    st.error("Password must be at least 6 characters.")
                else:
                    try:
                        res = requests.post(
                            f"{API_URL}/auth/register",
                            json={
                                "username": new_username,
                                "email": new_email,
                                "password": new_password
                            }
                        )
                        if res.status_code == 200:
                            st.success("✅ Account created successfully! Please login.")
                            st.session_state.auth_page = "login"
                            st.rerun()
                        else:
                            error_detail = res.json().get("detail", "Registration failed")
                            st.error(error_detail)
                    except Exception as e:
                        st.error(f"Cannot connect to backend: {e}")
        
        st.markdown("---")
        if st.button("⬅️ Back to Home", use_container_width=True):
            st.session_state.auth_page = None
            st.rerun()
        
        st.markdown("<p style='text-align: center; color: gray; margin-top: 1rem;'>Already have an account?</p>", unsafe_allow_html=True)
        if st.button("Login to Existing Account", use_container_width=True, key="switch_to_login"):
            st.session_state.auth_page = "login"
            st.rerun()

def main():
    """Main application entry point with routing logic."""
    
    # Initialize auth_page in session state if not present
    if "auth_page" not in st.session_state:
        st.session_state.auth_page = None
    
    # Check if user is logged in
    if "user" not in st.session_state:
        # Show homepage, login, or register based on auth_page state
        if st.session_state.auth_page == "login":
            show_login_page()
        elif st.session_state.auth_page == "register":
            show_register_page()
        else:
            show_homepage()
        return
    
    # User is logged in — show the main app
    user_id = st.session_state.user["id"]
    
    render_sidebar(user_id=user_id)
    
    tab1, tab2, tab3 = st.tabs(["💬 Chat & Mentor", "🗺️ Career Roadmap", "📊 Growth Analytics"])
    
    with tab1:
        render_chat(user_id=user_id)
    
    with tab2:
        render_roadmap(user_id=user_id)
        
    with tab3:
        render_visualizations(user_id=user_id)

if __name__ == "__main__":
    main()
