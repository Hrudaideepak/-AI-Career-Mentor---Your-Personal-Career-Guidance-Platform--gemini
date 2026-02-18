import google.generativeai as genai
from langchain_core.prompts import PromptTemplate
import os
import json
import asyncio

api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

# Using models/gemini-flash-latest which is confirmed available in this environment
model = genai.GenerativeModel('models/gemini-flash-latest')

async def extract_resume_details(text_content: str):
    prompt_template = """
    You are an expert resume analyzer. Extract the following details from the resume text below:
    - Skills (list)
    - Experience Level (Junior, Mid, Senior)
    - Years of Experience
    - Education
    
    Resume Text:
    {text}
    
    Return the result as a valid JSON object.
    """
    prompt = prompt_template.format(text=text_content)
    # Using loop.run_in_executor since genai is synchronous or use to_thread in 3.9+
    response = await asyncio.to_thread(model.generate_content, prompt)
    return response.text

async def generate_career_paths(user_skills: str, resume_content: str, experience_level: str):
    prompt_template = """
    You are a Personal AI Career Mentor. Based on the following user profile, suggest 3 suitable career paths.
    
    User Skills: {skills}
    Experience Level: {experience}
    Resume Summary: {resume}
    
    For each career path, provide:
    1. Career Name
    2. Why it is suitable
    3. Estimated Salary Range
    4. Required Additional Skills
    
    Return the result as a JSON list of objects.
    """
    prompt = prompt_template.format(skills=user_skills, experience=experience_level, resume=resume_content)
    response = await asyncio.to_thread(model.generate_content, prompt)
    return response.text

async def generate_chat_response(message: str, history_context: list, resume_context: list,
                                   cross_session_context: list = None, user_profile: str = "",
                                   session_summaries: str = ""):
    prompt_template = """
    You are a Personal AI Career Mentor. You have deep knowledge of this user from their resume and all past conversations.
    
    === USER PROFILE ===
    {user_profile}
    
    === RESUME CONTEXT ===
    {resume_ctx}
    
    === CURRENT SESSION HISTORY ===
    {history_ctx}
    
    === USER'S PAST SESSION SUMMARIES ===
    {session_summaries}
    
    === RELEVANT CONTEXT FROM ALL PAST CONVERSATIONS ===
    {cross_session_ctx}
    
    === USER'S CURRENT QUESTION ===
    {question}
    
    INSTRUCTIONS:
    - You remember everything this user has told you in ALL previous sessions.
    - Reference their specific skills, goals, and past discussions when relevant.
    - If they mentioned something in a previous session, acknowledge it naturally.
    - Be a helpful, encouraging, and personalized mentor. Keep it concise.
    """
    
    resume_ctx_str = "\n".join([doc for doc in resume_context]) if resume_context else "No resume uploaded yet."
    history_ctx_str = "\n".join([doc for doc in history_context]) if history_context else "This is the start of the conversation."
    cross_ctx_str = "\n".join([doc for doc in cross_session_context]) if cross_session_context else "No previous sessions."
    
    prompt = prompt_template.format(
        user_profile=user_profile or "Not available",
        resume_ctx=resume_ctx_str,
        history_ctx=history_ctx_str,
        session_summaries=session_summaries or "No past sessions.",
        cross_session_ctx=cross_ctx_str,
        question=message
    )
    response = await asyncio.to_thread(model.generate_content, prompt)
    return response.text

async def generate_roadmap(resume_text: str):
    prompt_template = """
    You are an expert Career Coach. Based on the user's resume below, generate a personalized career roadmap to help them advance in their field or transition to a better role.
    
    Resume:
    {resume}
    
    Create exactly 5 actionable steps. For EACH step, provide:
    - id (integer, starting from 1)
    - step (string, clear title of the step)
    - description (string, 2-3 sentence explanation of what to do and why it matters)
    - difficulty (string: "Beginner", "Intermediate", or "Advanced")
    - estimated_time (string, e.g. "2-4 weeks", "1-2 months")
    - status (string, always "pending")
    - resources (list of exactly 3 learning resources, each with):
        - title (string, name of the resource)
        - url (string, a real working URL — use well-known sites like coursera.org, udemy.com, freecodecamp.org, developer.mozilla.org, docs.python.org, youtube.com, github.com, medium.com, etc.)
        - type (string: "course", "article", "video", "book", or "tool")
    
    Return the result as a raw JSON list of objects. Do not include markdown formatting.
    """
    prompt = prompt_template.format(resume=resume_text)
    response = await asyncio.to_thread(model.generate_content, prompt)
    return response.text

async def analyze_skills(resume_text: str):
    prompt_template = """
    You are a Data Analyst for Career Growth. Analyze the resume below and extract the top 5 technical skills and estimate the user's proficiency level (0-100) based on experience years and project complexity.
    
    Resume:
    {resume}
    
    Return the result as a raw JSON object with keys:
    - "Skill": list of skill names
    - "Score": list of corresponding scores (0-100)
    
    Example format:
    {{
        "Skill": ["Python", "SQL"],
        "Score": [80, 60]
    }}
    Do not include markdown formatting.
    """
    prompt = prompt_template.format(resume=resume_text)
    response = await asyncio.to_thread(model.generate_content, prompt)
    return response.text
