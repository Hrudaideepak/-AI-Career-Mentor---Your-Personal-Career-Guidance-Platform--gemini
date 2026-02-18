import streamlit as st
import requests
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

def render_visualizations(user_id: int):
    st.header("📊 Growth & Progress Tracking")
    
    API_URL = "http://localhost:8000"
    data = {}
    
    try:
        with st.spinner("Analyzing your skills..."):
            response = requests.get(f"{API_URL}/analytics/{user_id}")
            if response.status_code == 200:
                analytics_data = response.json()
                # Transform to DataFrame format
                # The backend returns {"Skill": [], "Score": []}
                # We need to adapt it to the chart format. 
                # For simplicity, let's just show current proficiency for now.
                data = analytics_data
            elif response.status_code == 404:
                st.info("Please upload a resume to see analytics.")
                return
            else:
                st.error("Failed to load analytics.")
                return
    except Exception as e:
        st.error(f"Error fetching analytics: {e}")
        return
    
    # Current proficiency (Radar/Bar Chart)
    if data:
        st.subheader("Current Skill Proficiency")
        # Ensure lists are same length
        if len(data.get("Skill", [])) > 0:
            df = pd.DataFrame(data)
            fig_bar = px.bar(df, x="Skill", y="Score", color="Skill", title="Estimated Proficiency (0-100)")
            st.plotly_chart(fig_bar, use_container_width=True)
        else:
            st.warning("No skills detected yet.")
