import streamlit as st
import requests

def render_roadmap(user_id: int):
    st.header("🗺️ Career Roadmap")
    
    API_URL = "http://localhost:8000"
    roadmap_steps = []
    
    try:
        with st.spinner("Generating your personalized roadmap..."):
            response = requests.get(f"{API_URL}/roadmap/{user_id}")
            if response.status_code == 200:
                roadmap_steps = response.json()
            elif response.status_code == 404:
                st.info("📄 Please upload a resume first to generate your personalized roadmap.")
                return
            else:
                st.error("Failed to load roadmap.")
                return
    except Exception as e:
        st.error(f"Error fetching roadmap: {e}")
        return
    
    if not roadmap_steps:
        st.info("No roadmap data available.")
        return
    
    # Initialize completion tracking in session state
    if "roadmap_completed" not in st.session_state:
        st.session_state.roadmap_completed = set()
    
    # --- Progress Bar ---
    total = len(roadmap_steps)
    completed_count = sum(1 for s in roadmap_steps if s.get("id") in st.session_state.roadmap_completed)
    progress = completed_count / total if total > 0 else 0
    
    prog_col1, prog_col2 = st.columns([4, 1])
    with prog_col1:
        st.progress(progress)
    with prog_col2:
        st.markdown(f"**{completed_count} / {total} completed**")
    
    st.markdown("---")
    
    # Icons for resource types
    type_icons = {
        "course": "📚",
        "article": "📄",
        "video": "🎬",
        "book": "📖",
        "tool": "🛠️",
    }
    
    # Colors for difficulty levels
    difficulty_badges = {
        "Beginner": "🟢 Beginner",
        "Intermediate": "🟡 Intermediate",
        "Advanced": "🔴 Advanced",
    }
    
    # --- Render Each Step ---
    for step in roadmap_steps:
        step_id = step.get("id", 0)
        is_completed = step_id in st.session_state.roadmap_completed
        title = step.get("step", "Untitled Step")
        
        # Build expander label
        status_prefix = "✅" if is_completed else f"📌 Step {step_id}"
        
        with st.expander(f"{status_prefix} — {title}", expanded=not is_completed):
            # Description
            description = step.get("description", "")
            if description:
                st.markdown(description)
            
            # Metadata row: difficulty + estimated time
            difficulty = step.get("difficulty", "Intermediate")
            est_time = step.get("estimated_time", "N/A")
            badge = difficulty_badges.get(difficulty, f"⚪ {difficulty}")
            
            meta_col1, meta_col2 = st.columns(2)
            with meta_col1:
                st.markdown(f"**Difficulty:** {badge}")
            with meta_col2:
                st.markdown(f"**⏱️ Estimated Time:** {est_time}")
            
            st.markdown("")
            
            # Learning Resources
            resources = step.get("resources", [])
            if resources:
                st.markdown("#### 📖 Learning Resources")
                for res in resources:
                    icon = type_icons.get(res.get("type", ""), "🔗")
                    res_title = res.get("title", "Resource")
                    url = res.get("url", "#")
                    res_type = res.get("type", "resource").capitalize()
                    st.markdown(f"- {icon} [{res_title}]({url}) — *{res_type}*")
            
            st.markdown("")
            
            # Mark as complete button
            if not is_completed:
                if st.button(f"✅ Mark Step {step_id} as Complete", key=f"complete_{step_id}"):
                    st.session_state.roadmap_completed.add(step_id)
                    st.rerun()
            else:
                st.success("You've completed this step! Great progress! 🎉")
