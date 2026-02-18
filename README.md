# 🎯 AI Career Mentor - Your Personal Career Guidance Platform

**Created by: Hrudai deepak Bonagiri**

---

## 📖 What Is This Project?

Hey there! Let me tell you about this project I built. Imagine having a personal career mentor who knows everything about you - your resume, your skills, your career goals, and even remembers every conversation you've had with them across multiple sessions. That's exactly what this AI Career Mentor does!

This is a full-stack web application that combines:

- **AI-powered career guidance** using OpenAI's GPT-4o-mini
- **Smart memory system** that remembers your resume and all past conversations
- **Personalized roadmaps** with actual learning resources to help you grow
- **Career analytics** showing your skill proficiency
- **Session management** where you can have up to 10 different conversation threads

Think of it as having a career coach in your pocket who never forgets anything about you and gives advice based on your actual resume and history.

---

## 🌟 Key Features I Built

### 1. **User Authentication System**

- You can register your own account with username, email, and password
- Passwords are securely hashed using bcrypt (no plain text storage!)
- Each user gets their own isolated space - your data never mixes with others

### 2. **AI Chat with Memory**

- Chat with GPT-4o-mini that actually knows your background
- The AI remembers your resume, past conversations, and goals
- Up to 10 separate conversation sessions per user (oldest auto-deleted when you hit 11)
- Session numbers are per-user (your Session 1 is YOUR Session 1, not a global ID)

### 3. **Smart Context System**

I implemented a sophisticated context system using ChromaDB (a vector database):

- Your resume gets embedded and stored
- All your chat messages get embedded too
- When you ask a question, the AI searches through:
  - Your resume (to know your skills)
  - Current session history (conversation flow)
  - ALL your past sessions (cross-session awareness!)
  - Session summaries (bird's eye view of what you discussed)

### 4. **Career Roadmap Generator**

- Upload resume → AI creates a 5-step personalized career roadmap
- Each step includes:
  - What to do and why it matters
  - Difficulty level (Beginner/Intermediate/Advanced)
  - Estimated time (e.g., "2-4 weeks")
  - 3 real learning resources with working URLs
  - Progress tracking (mark steps as complete)

### 5. **Skill Analytics Dashboard**

- Visual charts showing your top 5 skills
- Proficiency scores (0-100) estimated from your resume
- Helps you see where you're strong and where to improve

### 6. **Resume Upload & Analysis**

- Upload PDF, TXT, CSV, JPG, or PNG files
- AI extracts your skills, experience, education automatically
- Stored in both PostgreSQL (structured data) and ChromaDB (for AI search)

---

## 🏗️ How This Project Works (The Big Picture)

Let me walk you through the architecture I designed:

```
┌─────────────┐
│   Browser   │ ← You interact here (Streamlit UI on localhost:8501)
└──────┬──────┘
       │
       ↓ HTTP Requests
┌─────────────────┐
│   FastAPI       │ ← Backend server (localhost:8000)
│   Backend       │    - Handles authentication, sessions, chat logic
└────┬────┬───────┘
     │    │
     │    └──────→ ┌──────────────┐
     │             │  PostgreSQL  │ ← Stores users, sessions, messages, resumes
     │             │  Database    │    (Relational data)
     │             └──────────────┘
     │
     └──────→ ┌──────────────┐
              │  ChromaDB    │ ← Stores embeddings for AI search
              │  Vector DB   │    (Semantic search)
              └──────┬───────┘
                     │
                     ↓ Queries
              ┌──────────────┐
              │  OpenAI API  │ ← GPT-4o-mini generates responses
              │  GPT-4o-mini │
              └──────────────┘
```

**The Flow When You Chat:**

1. You type a message in Streamlit → Sent to FastAPI `/chat/messages/`
2. FastAPI saves your message to PostgreSQL
3. FastAPI embeds your message and stores it in ChromaDB
4. FastAPI queries ChromaDB for:
   - Relevant resume context
   - Current session chat history
   - Cross-session chat history (all your past convos)
5. FastAPI builds a rich prompt with all context and sends to OpenAI
6. OpenAI returns smart response (it has full context about you!)
7. FastAPI saves AI response to PostgreSQL + ChromaDB
8. Response sent back to Streamlit → You see it

**Why I Did It This Way:**

- **PostgreSQL** for structured data (users, sessions) - fast queries, relationships
- **ChromaDB** for semantic search - finds relevant context even if words don't match exactly
- **OpenAI** for intelligence - generates human-like advice
- **Streamlit** for UI - quick to build, looks professional

---

## 🛠️ Technology Stack I Used

### Backend (Python)

- **FastAPI** (0.129.0) - Modern REST API framework, super fast
- **SQLAlchemy** (2.0.46) - ORM for database operations
- **Psycopg2** (2.9.10) - PostgreSQL adapter
- **Bcrypt** (4.3.0) - Password hashing
- **Python-Jose** (3.3.0) - JWT token handling (for future auth expansion)
- **Python-Multipart** (0.0.20) - File upload handling

### AI & ML

- **LangChain-OpenAI** (0.3.9) - Wrapper for OpenAI API
- **ChromaDB** (1.5.0) - Vector database for embeddings
- **OpenAI** (via LangChain) - GPT-4o-mini for AI responses

### Frontend (Python)

- **Streamlit** (1.54.0) - Web UI framework
- **Requests** (2.32.3) - HTTP client to call backend

### Database

- **PostgreSQL 18** - Main database

### Dev Tools

- **uv** - Modern Python package manager (faster than pip)
- **python-dotenv** (1.0.1) - Environment variable management

---

## 📁 Project Structure Explained (Every File!)

```
AI Career Recommender/
│
├── .env                    ← Configuration file (API keys, DB credentials)
├── .python-version         ← Locks Python to 3.11 (uv uses this)
├── pyproject.toml          ← Dependencies and project metadata
├── uv.lock                 ← Locked dependency versions (reproducible installs)
├── requirements.txt        ← Backup dependency list (for pip users)
├── migrate_db.py           ← Database migration script (adds new columns to existing DB)
├── seed_db.py              ← Creates test user (testuser/password123)
├── README.md               ← This file you're reading!
│
├── backend/                ← FastAPI backend server
│   └── app/
│       ├── main.py         ← FastAPI app entry point, includes all routers
│       ├── database.py     ← SQLAlchemy engine and session setup
│       ├── models.py       ← Database table definitions (User, ChatSession, etc.)
│       ├── schemas.py      ← Pydantic models for request/response validation
│       ├── crud.py         ← Database operations (create user, get sessions, etc.)
│       ├── auth.py         ← Password hashing and verification (bcrypt)
│       │
│       ├── routers/        ← API endpoints (each file is a group of related routes)
│       │   ├── __init__.py
│       │   ├── auth.py     ← /auth/login, /auth/register
│       │   ├── chat.py     ← /chat/sessions/, /chat/messages/, /chat/history/{session_id}
│       │   ├── resume.py   ← /resumes/upload/{user_id}
│       │   ├── roadmap.py  ← /roadmap/{user_id}
│       │   ├── analytics.py← /analytics/{user_id}
│       │   ├── career.py   ← /career/recommend/{user_id}
│       │   └── progress.py ← /progress/{user_id}
│       │
│       └── services/       ← Business logic and external integrations
│           ├── openai_service.py   ← All OpenAI API calls (chat, roadmap, analytics)
│           ├── chroma_service.py   ← ChromaDB operations (add, query embeddings)
│           └── parser_service.py   ← Resume file parsing (PDF, TXT, images)
│
├── frontend/               ← Streamlit web UI
│   ├── app.py              ← Main entry point (routing between home/login/register/app)
│   └── components/         ← Reusable UI components
│       ├── sidebar.py      ← Left sidebar (profile, chat history, resume upload)
│       ├── chat_ui.py      ← Chat interface (message input, history display)
│       ├── roadmap_ui.py   ← Career roadmap display (steps, resources, progress)
│       └── visualizations.py ← Skill analytics charts
│
└── data/                   ← Application data (auto-created)
    ├── chroma_db/          ← ChromaDB embeddings storage
    └── resumes/            ← Uploaded resume files (organized by user_id)
```

---

## 🔍 Detailed File Breakdown

### Backend Files

#### **`backend/app/main.py`** - The Commander

This is where everything starts. When you run `uvicorn app.main:app`, this file:

- Creates the FastAPI application instance
- Includes all routers (auth, chat, resume, roadmap, analytics, career, progress)
- Sets up CORS (allows frontend on port 8501 to call backend on port 8000)
- Has a root endpoint `/` that says "AI Career Recommender API is running"

**Key function:**

```python
app = FastAPI(title="AI Career Recommender API")
app.include_router(auth_router)  # Adds all /auth/* endpoints
app.include_router(chat_router)  # Adds all /chat/* endpoints
# ... and so on
```

#### **`backend/app/database.py`** - The Bridge to PostgreSQL

Sets up SQLAlchemy engine and session factory.

**What it does:**

- Reads `DATABASE_URL` from `.env`
- Creates engine (connection pool to PostgreSQL)
- `SessionLocal()` - factory to get a database session
- `Base` - all models inherit from this to become tables

**Key code:**

```python
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()  # Models inherit from this
```

#### **`backend/app/models.py`** - The Database Blueprint

Defines 8 tables using SQLAlchemy ORM:

1. **`User`** - Stores user accounts
   - `id`, `username`, `email`, `hashed_password`, `created_at`
   - Relationships: `chat_sessions`, `resumes`, `career_recommendations`, `progress_tracking`, `roadmaps`

2. **`ChatSession`** - Conversation threads
   - `id`, `user_id`, `session_number` (1-10 per user), `resume_id`, `created_at`, `summary`
   - **Why session_number?** So each user sees "Session 1, 2, 3..." instead of global DB IDs

3. **`ChatMessage`** - Individual messages
   - `id`, `session_id`, `user_id`, `role` (user/assistant), `content`, `timestamp`

4. **`Resume`** - Uploaded resumes
   - `id`, `user_id`, `file_path`, `parsed_content`, `uploaded_at`

5. **`CareerRecommendation`** - AI-generated career paths
   - `id`, `user_id`, `career_name`, `reasoning`, `salary_range`, `created_at`

6. **`ProgressTracking`** - Skill proficiency scores
   - `id`, `user_id`, `skill_name`, `score`, `date`

7. **`Roadmap`** - Career roadmaps
   - `id`, `user_id`, `career_id`, `title`, `created_at`

8. **`RoadmapStep`** - Individual steps in roadmap
   - `id`, `roadmap_id`, `step_name`, `status`, `completion_date`

**Why these tables?** Relational data (who owns what, links between entities) is best in PostgreSQL.

#### **`backend/app/schemas.py`** - The Validators

Pydantic models that validate incoming/outgoing data.

**Example:**

```python
class UserRegister(BaseModel):
    username: str
    email: str
    password: str  # Won't be stored as-is, gets hashed
```

When frontend sends JSON to `/auth/register`, FastAPI automatically:

- Checks all fields are present
- Validates types (username is string, etc.)
- Returns 422 error if validation fails

**Why separate from models.py?**

- Models = database structure
- Schemas = API contracts (what you send/receive)
- They're similar but serve different purposes

#### **`backend/app/crud.py`** - The Database Worker

CRUD = Create, Read, Update, Delete. All database operations live here.

**Key functions I wrote:**

1. **`create_chat_session(db, session)`**
   - Counts existing sessions for user
   - If user has 10 sessions, deletes oldest + renumbers others 1-9
   - Creates new session as number 10
   - **Why?** Prevents unlimited session buildup, keeps it clean

2. **`get_chat_sessions(db, user_id)`**
   - Returns all sessions for a user, ordered by `session_number`

3. **`get_all_user_chat_messages(db, user_id, limit=50)`**
   - Gets recent messages across ALL sessions for a user
   - Used for cross-session AI context

4. **`get_user_by_username(db, username)`**
   - Looks up user for login

5. **`create_chat_message(db, message)`**
   - Saves a message to database

**Why a separate CRUD file?** Keeps database logic separate from API routes. Clean code!

#### **`backend/app/auth.py`** - The Security Guard

Handles password hashing and verification.

**Functions:**

1. **`get_password_hash(password)`**
   - Takes plain password (e.g., "password123")
   - Truncates to 72 bytes (bcrypt limitation)
   - Generates bcrypt hash (e.g., "$2b$12$abc123...")
   - Returns hash string

2. **`verify_password(plain_password, hashed_password)`**
   - Takes plain password + stored hash
   - Returns True if match, False otherwise

**Why bcrypt?** Industry standard, slow by design (prevents brute force attacks), automatic salting.

**Why [:72] truncation?** Bcrypt can only handle 72 bytes. If someone pastes a 1000-character password, we truncate it first.

#### **`backend/app/routers/auth.py`** - Login & Registration API

**Endpoints:**

1. **`POST /auth/register`**

   ```json
   {
     "username": "krishna123",
     "email": "krishna@example.com",
     "password": "mypass"
   }
   ```

   - Checks if username/email already exists (returns 400 if yes)
   - Hashes password
   - Creates user in database
   - Returns user data (without password!)

2. **`POST /auth/login`**

   ```json
   {
     "username": "krishna123",
     "password": "mypass"
   }
   ```

   - Finds user by username
   - Verifies password
   - Returns user data if correct (401 if wrong)

**Why no JWT tokens?** I kept it simple for now. In production, you'd return a JWT token and require it for all protected routes.

#### **`backend/app/routers/chat.py`** - The Brain of the Chat System

**Endpoints:**

1. **`POST /chat/sessions/`** - Creates new session
2. **`GET /chat/sessions/{user_id}`** - Gets all sessions for user
3. **`GET /chat/history/{session_id}`** - Gets messages in a session
4. **`POST /chat/messages/`** - The main endpoint, handles sending a message

**The `/chat/messages/` Flow (Most Complex Part):**

```python
async def create_message(message: ChatMessageCreate, db: Session):
    # 1. Save user message to PostgreSQL
    db_message = crud.create_chat_message(db, message)

    # 2. Add to ChromaDB for future semantic search
    chroma_service.add_chat_to_vector_store(...)

    # 3. Gather context for AI:

    # 3a. Get resume context (user's skills, experience)
    resume_context = chroma_service.query_resume_context(message.content, user_id, resume_id)

    # 3b. Get current session history (recent conversation flow)
    history_context = chroma_service.query_chat_history(message.content, session_id)

    # 3c. Get cross-session context (what user discussed in ALL past sessions)
    cross_session_context = chroma_service.query_user_chat_history(message.content, user_id)

    # 3d. Get user profile (username, email)
    user_profile = "Username: krishna123, Email: krishna@example.com"

    # 3e. Get summaries of all sessions
    session_summaries = "Session 1: Discussed career switch to ML..."

    # 4. Call OpenAI with ALL context
    ai_response = await openai_service.generate_chat_response(
        message.content,
        history_context,
        resume_context,
        cross_session_context,
        user_profile,
        session_summaries
    )

    # 5. Save AI response to PostgreSQL + ChromaDB
    # 6. Return AI response
```

**Why so much context?** The AI needs to know EVERYTHING about you to give personalized advice. It's the difference between a generic chatbot and a personal mentor.

#### **`backend/app/routers/resume.py`** - Resume Upload Handler

**Endpoint: `POST /resumes/upload/{user_id}`**

**What happens:**

1. Receives file (PDF, TXT, CSV, image)
2. Saves to `data/resumes/{user_id}/{filename}` (auto-creates folders)
3. Parses file content (extracts text using `parser_service`)
4. Saves to PostgreSQL (`Resume` table)
5. Asks OpenAI to extract skills, experience, education
6. Embeds resume text and stores in ChromaDB (for semantic search)
7. Optionally links resume to current chat session

**Why save the file?** Could just parse and discard, but saving allows:

- User to re-download later
- Audit trail
- Re-processing if needed

**Path resolution trick:**

```python
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
RESUMES_DIR = PROJECT_ROOT / "data" / "resumes"
```

This ensures files ALWAYS go to `root/data/resumes/` regardless of where you run uvicorn from.

#### **`backend/app/routers/roadmap.py`** - Career Roadmap Generator

**Endpoint: `GET /roadmap/{user_id}`**

**Flow:**

1. Gets user's latest resume from database
2. Sends resume to OpenAI via `openai_service.generate_roadmap()`
3. OpenAI returns 5-step roadmap JSON
4. Saves roadmap + steps to database
5. Returns roadmap

**Roadmap structure:**

```json
[
  {
    "id": 1,
    "step": "Enhance Cloud Skills",
    "description": "Learn AWS, Azure...",
    "difficulty": "Intermediate",
    "estimated_time": "1-2 months",
    "status": "pending",
    "resources": [
      {
        "title": "AWS Certified Solutions Architect",
        "url": "https://www.coursera.org/...",
        "type": "course"
      }
    ]
  }
]
```

**Why generate fresh each time?** Could cache, but resume might change, so regenerating ensures accuracy.

#### **`backend/app/routers/analytics.py`** - Skill Dashboard

**Endpoint: `GET /analytics/{user_id}`**

Extracts top 5 skills + scores from resume using OpenAI, returns:

```json
{
  "Skill": ["Python", "SQL", "FastAPI", "Docker", "AWS"],
  "Score": [85, 70, 65, 60, 55]
}
```

Frontend turns this into a bar chart.

#### **`backend/app/routers/career.py`** - Career Recommendations

**Endpoint: `GET /career/recommend/{user_id}`**

Sends resume to OpenAI asking for 3 suitable career paths with reasoning and salary ranges.

#### **`backend/app/routers/progress.py`** - Progress Tracking

**Endpoint: `POST /progress/`**

Saves skill proficiency scores to database (for future features like progress over time).

#### **`backend/app/services/openai_service.py`** - The AI Caller

All OpenAI API interactions happen here. I organized it into functions:

1. **`extract_resume_details(text_content)`**
   - Sends resume text to GPT-4o-mini
   - Asks to extract skills, experience level, years, education
   - Returns JSON

2. **`generate_career_paths(user_skills, resume_content, experience_level)`**
   - Asks for 3 career recommendations
   - Returns structured JSON

3. **`generate_chat_response(message, history_context, resume_context, cross_session_context, user_profile, session_summaries)`**
   - **The main chat function**
   - Builds a detailed prompt:

     ```
     You are a Personal AI Career Mentor. You have deep knowledge of this user...

     === USER PROFILE ===
     Username: krishna123, Email: krishna@example.com

     === RESUME CONTEXT ===
     Python developer with 3 years experience...

     === CURRENT SESSION HISTORY ===
     User: How do I learn ML?
     Assistant: Start with Python basics...

     === USER'S PAST SESSION SUMMARIES ===
     Session 1: Discussed career switch to ML...
     Session 2: Asked about salary expectations...

     === RELEVANT CONTEXT FROM ALL PAST CONVERSATIONS ===
     "I want to transition to data science" (from Session 1)
     "I know Python and SQL" (from Session 2)

     === USER'S CURRENT QUESTION ===
     What courses should I take for ML?

     INSTRUCTIONS:
     - You remember EVERYTHING this user has told you in ALL previous sessions.
     - Reference their specific skills, goals, and past discussions.
     - Be a helpful, encouraging, personalized mentor.
     ```

   - Sends to OpenAI
   - Returns response

4. **`generate_roadmap(resume_text)`**
   - Prompt asks for 5 steps, each with description, difficulty, time, and 3 learning resources
   - Returns JSON

5. **`analyze_skills(resume_text)`**
   - Extracts top 5 skills + proficiency scores (0-100)
   - Returns JSON

**Why separate service file?** Keeps AI logic separate from API routes. If you switch from OpenAI to another LLM, you only change this file.

#### **`backend/app/services/chroma_service.py`** - The Memory System

ChromaDB is a vector database. It converts text to embeddings (arrays of numbers) and allows semantic search.

**Collections:**

- `resume_embeddings` - Stores resume texts
- `chat_history_embeddings` - Stores all chat messages

**Functions:**

1. **`add_resume_to_vector_store(resume_text, user_id, resume_id)`**
   - Embeds resume using OpenAI's `text-embedding-ada-002`
   - Stores with metadata: `{"user_id": "1", "resume_id": "5"}`
   - Allows future queries like "find resumes for user 1"

2. **`query_resume_context(query_text, user_id, resume_id=None, n_results=2)`**
   - Takes user's question (e.g., "What are my skills?")
   - Searches resume embeddings for user
   - Returns most relevant resume chunks

3. **`add_chat_to_vector_store(chat_text, user_id, session_id, message_id)`**
   - Embeds chat message
   - Stores with metadata: `{"user_id": "1", "session_id": "3"}`

4. **`query_chat_history(query_text, session_id, n_results=5)`**
   - Searches messages in a specific session
   - Returns most relevant messages (semantic search!)

5. **`query_user_chat_history(query_text, user_id, n_results=10)`**
   - **Cross-session search** - searches ALL messages for a user
   - Example: User asks "What did I say about salaries?" in Session 5
   - This function finds "I want a $100k salary" from Session 2

**Path resolution trick:**

```python
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
CHROMA_DB_PATH = str(PROJECT_ROOT / "data" / "chroma_db")
```

Ensures ChromaDB always writes to `root/data/chroma_db/` regardless of working directory.

**Why ChromaDB?** Could use traditional database search, but:

- Semantic search: "What did I say about pay?" finds "I discussed salary..."
- Fast with large data
- Automatic embedding (no manual feature engineering)

#### **`backend/app/services/parser_service.py`** - File Reader

**Function: `parse_resume(file: UploadFile)`**

Supports:

- PDF (PyPDF2)
- TXT (plain text)
- CSV (pandas)
- Images JPG/PNG (pytesseract OCR)

Returns extracted text as string.

**Why different parsers?** People upload resumes in various formats. This handles all common ones.

---

### Frontend Files

#### **`frontend/app.py`** - The UI Router

This is the main entry point when you run `streamlit run app.py`.

**Pages:**

1. **Homepage** (`show_homepage()`)
   - Hero section with project description
   - Feature overview (AI Chat, Roadmap, Analytics, Resume Upload)
   - "How It Works" section
   - Tech stack showcase
   - Login/Register buttons

2. **Login Page** (`show_login_page()`)
   - Username + password form
   - Calls `/auth/login` API
   - Stores user data in `st.session_state.user`
   - Redirects to main app on success

3. **Register Page** (`show_register_page()`)
   - Username + email + password + confirm password form
   - Calls `/auth/register` API
   - Redirects to login page on success

4. **Main App** (when logged in)
   - Shows sidebar with profile, chat history, resume upload
   - 3 tabs:
     - **Chat & Mentor** - AI chat interface
     - **Career Roadmap** - Personalized steps
     - **Growth Analytics** - Skill charts

**Routing logic:**

```python
def main():
    if "user" not in st.session_state:
        # Not logged in
        if st.session_state.auth_page == "login":
            show_login_page()
        elif st.session_state.auth_page == "register":
            show_register_page()
        else:
            show_homepage()
    else:
        # Logged in, show main app
        render_sidebar(user_id)
        # ... tabs ...
```

**Session state:** Streamlit's session state persists data across reruns (like React state).

#### **`frontend/components/sidebar.py`** - Left Sidebar

**Sections:**

1. **Profile**
   - Shows username + email
   - Logout button (clears `st.session_state` and reloads)

2. **Chat History**
   - Fetches sessions from `/chat/sessions/{user_id}`
   - Displays buttons: "Session 1 - How do I learn ML..."
   - Shows session count: "5 / 10 sessions used"
   - "New Chat" button creates fresh session

3. **Resume Upload**
   - File uploader (PDF, TXT, CSV, JPG, PNG)
   - "Analyze Resume" button → calls `/resumes/upload/{user_id}`
   - Success message on upload

**Key code:**

```python
for session in sessions:
    session_num = session.get('session_number', session['id'])
    if st.button(f"Session {session_num} - {summary}"):
        st.session_state.current_session_id = session['id']
        st.rerun()  # Reload page to show that session's messages
```

#### **`frontend/components/chat_ui.py`** - Chat Interface

**Functionality:**

1. **Load history** (if switching to existing session)

   ```python
   if current_session_id:
       history = requests.get(f"/chat/history/{current_session_id}").json()
       for msg in history:
           st.session_state.messages.append(msg)
   ```

2. **Input form** at top
   - Text input + Send button
   - `clear_on_submit=True` empties input after sending

3. **Send message**
   - If no session exists, create one first (`POST /chat/sessions/`)
   - Send message to `/chat/messages/`
   - Append user message + AI response to `st.session_state.messages`
   - Rerun to display

4. **Display messages**
   ```python
   for message in st.session_state.messages:
       with st.chat_message(message["role"]):  # Shows user/assistant icons
           st.markdown(message["content"])
   ```

**Why `st.session_state.messages`?** Streamlit reruns the entire script on every interaction. Session state preserves the message list across reruns.

#### **`frontend/components/roadmap_ui.py`** - Roadmap Display

**Features:**

1. **Fetch roadmap** from `/roadmap/{user_id}`
2. **Progress bar** showing completed steps / total
3. **Expandable steps** (`st.expander()`)
   - Shows description, difficulty, estimated time
   - Learning resources as clickable links with type icons (📚 course, 📄 article, 🎥 video)
   - Checkbox to mark complete (stored in `st.session_state`)

**Progress calculation:**

```python
completed = sum(1 for step_id, done in st.session_state.completed_steps.items() if done)
total = len(roadmap_steps)
progress = completed / total
st.progress(progress)
```

**Why expandable?** Keeps UI clean, shows summary first, details on click.

#### **`frontend/components/visualizations.py`** - Analytics Charts

**Displays:**

1. **Bar chart** - Top 5 skills with proficiency scores

   ```python
   chart_data = pd.DataFrame({"Skill": [...], "Score": [...]})
   st.bar_chart(chart_data.set_index("Skill"))
   ```

2. **Insight text** - "Your strongest skill is Python (85%)"

Fetches data from `/analytics/{user_id}`.

**Why Altair/built-in charts?** Streamlit has simple chart functions that look professional without complex code.

---

### Support Files

#### **`.env`** - Configuration File (YOU MUST EDIT THIS!)

```dotenv
# Database Configuration
DATABASE_URL=postgresql://postgres:yourpassword@localhost:5432/career_db

# OpenAI Configuration
OPENAI_API_KEY="your-actual-openai-api-key-here"

# ChromaDB Configuration (auto-resolved to root/data/chroma_db)
# CHROMA_DB_PATH is now computed in code
```

**What to change:**

- `postgres:yourpassword` → Your PostgreSQL password (e.g., `postgres:root`)
- `OPENAI_API_KEY` → Your OpenAI API key from platform.openai.com

**Why .env?** Keeps secrets out of code. Never commit this to Git!

#### **`pyproject.toml`** - Project Metadata

Defines:

- Project name, version, description
- Python version requirement (3.11+)
- Dependencies (18 packages)

**Key section:**

```toml
[tool.uv]
package = false  # This is an app, not a library
```

**Why `package = false`?** Tells uv not to try installing the project itself as a package (would fail with flat layout).

#### **`uv.lock`** - Locked Dependencies

Auto-generated by uv. Lists exact versions + checksums of every dependency (including transitive ones). Ensures reproducible installs.

Don't edit manually.

#### **`migrate_db.py`** - Database Migrations

Adds new columns to existing database without losing data.

**Migrations:**

1. Adds `resume_id` to `chat_sessions` (links session to specific resume)
2. Adds `hashed_password` to `users` (for authentication)
3. Adds `session_number` to `chat_sessions` (per-user session numbering)
4. Backfills `session_number` for existing sessions

Run this AFTER changing models.py and BEFORE running the app.

**Why not drop/recreate tables?** Would lose all data. Migrations preserve existing data while updating schema.

#### **`seed_db.py`** - Test Data Creator

Creates:

- All tables (if they don't exist)
- Test user: `testuser` / `password123`

Run this once on fresh database to get a working login.

**Why a test user?** Lets you test the app immediately without registering.

---

## 💾 Database Schema

**Tables:**

```
users
├── id (PK)
├── username (unique)
├── email (unique)
├── hashed_password
└── created_at

chat_sessions
├── id (PK)
├── user_id (FK → users.id)
├── session_number (1-10 per user)
├── resume_id (FK → resumes.id, nullable)
├── created_at
└── summary

chat_messages
├── id (PK)
├── session_id (FK → chat_sessions.id)
├── user_id (FK → users.id)
├── role (user/assistant)
├── content
└── timestamp

resumes
├── id (PK)
├── user_id (FK → users.id)
├── file_path
├── parsed_content
└── uploaded_at

career_recommendations
├── id (PK)
├── user_id (FK → users.id)
├── career_name
├── reasoning
├── salary_range
└── created_at

progress_tracking
├── id (PK)
├── user_id (FK → users.id)
├── skill_name
├── score
└── date

roadmaps
├── id (PK)
├── user_id (FK → users.id)
├── career_id (FK → career_recommendations.id, nullable)
├── title
└── created_at

roadmap_steps
├── id (PK)
├── roadmap_id (FK → roadmaps.id)
├── step_name
├── status (pending/completed)
└── completion_date
```

**Relationships:**

- One user has many sessions, messages, resumes, roadmaps
- One session has many messages
- One roadmap has many steps

---

## 🚀 Setup Guide (From ZIP to Running App)

Alright, let's get this thing running on your machine! I'll assume you know NOTHING and walk you through every step.

### Prerequisites (Install These First)

1. **Python 3.11 or higher**
   - Download from python.org
   - During install, CHECK "Add Python to PATH"
   - Verify: Open Command Prompt/Terminal, type `python --version`
   - Should show: `Python 3.11.x` or higher

2. **PostgreSQL 18** (or any recent version)
   - Download from postgresql.org
   - During install:
     - Set password for `postgres` user (remember this!)
     - Default port 5432 is fine
   - Add PostgreSQL bin folder to PATH:
     - **Windows:** `C:\Program Files\PostgreSQL\18\bin`
     - **Mac:** Already in PATH
     - **Linux:** Already in PATH
   - Verify: `psql --version` in terminal

3. **uv** (Modern Python Package Manager)
   - **Windows PowerShell:** `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"`
   - **Mac/Linux:** `curl -LsSf https://astral.sh/uv/install.sh | sh`
   - Restart terminal
   - Verify: `uv --version`

4. **OpenAI API Key**
   - Go to platform.openai.com
   - Sign up / Log in
   - Go to API Keys section
   - Click "Create new secret key"
   - Copy it (starts with `sk-...`)
   - **You'll need this later!**

### Step 1: Extract the ZIP

Extract `AI Career Recommender.zip` to a folder, e.g., `C:\Projects\AI Career Recommender\` (Windows) or `~/projects/ai-career-recommender/` (Mac/Linux).

### Step 2: Create PostgreSQL Database

Open terminal/Command Prompt:

```bash
# Connect to PostgreSQL
psql -U postgres

# Enter your postgres password when prompted

# Create database
CREATE DATABASE career_db;

# Verify it's created
\l

# Exit
\q
```

**What does this do?** Creates an empty database named `career_db` where all your data will live.

### Step 3: Configure Environment Variables

Open `.env` file in a text editor (VS Code, Notepad++, etc.)

**Change these lines:**

```dotenv
# BEFORE (default)
DATABASE_URL=postgresql://postgres:postres@localhost:5432/career_db
OPENAI_API_KEY="your_openai_api_key_here"

# AFTER (your actual values)
DATABASE_URL=postgresql://postgres:YOUR_POSTGRES_PASSWORD@localhost:5432/career_db
OPENAI_API_KEY="sk-proj-abc123YOUR_ACTUAL_OPENAI_KEY_xyz"
```

**Example:**

- If your PostgreSQL password is `root`, change to: `postgresql://postgres:root@localhost:5432/career_db`
- Paste your OpenAI key between quotes

**Save the file!**

### Step 4: Install Python Dependencies

Open terminal in the project root folder:

```bash
# Navigate to project folder
cd "C:\Projects\AI Career Recommender"  # Windows
cd ~/projects/ai-career-recommender     # Mac/Linux

# Install dependencies using uv (fast!)
uv sync

# This will:
# - Create a .venv folder with isolated Python environment
# - Install all 18+ packages and their dependencies
# - Takes 30-60 seconds
```

**What does `uv sync` do?** Reads `pyproject.toml`, creates a virtual environment (`.venv/`), installs all packages.

**Troubleshooting:**

- If `uv sync` fails: Try `uv pip install -r requirements.txt`
- If `uv` not found: Restart terminal after installing uv

### Step 5: Run Database Migrations

This creates all 8 tables in your database.

```bash
# Still in project root
uv run python migrate_db.py
```

**Expected output:**

```
Attempting to add resume_id column...
resume_id migration skipped (already exists): ...
Attempting to add hashed_password column...
hashed_password migration skipped (already exists): ...
Attempting to add session_number column...
Migration successful: Added session_number to chat_sessions.
Backfill successful: session_number updated for all existing sessions.
```

**What happened?** Script added columns to tables. "Already exists" messages are normal if you run it multiple times.

### Step 6: Create Test User (Optional but Recommended)

```bash
uv run python seed_db.py
```

**Output:**

```
Database tables created!
Test user created/updated: testuser / password123
```

**What happened?** Created a user you can login with immediately (username: `testuser`, password: `password123`).

### Step 7: Start the Backend Server

Open a new terminal (keep it running):

```bash
cd "C:\Projects\AI Career Recommender\backend"  # Windows
cd ~/projects/ai-career-recommender/backend     # Mac/Linux

uv run uvicorn app.main:app --reload
```

**Expected output:**

```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Application startup complete.
```

**What does this do?** Starts FastAPI server on port 8000. The `--reload` flag auto-restarts when you edit code (dev mode).

**Test it:** Open browser, go to `http://localhost:8000` → Should see `{"message": "AI Career Recommender API is running"}`

### Step 8: Start the Frontend Server

Open ANOTHER new terminal (backend should still be running):

```bash
cd "C:\Projects\AI Career Recommender\frontend"  # Windows
cd ~/projects/ai-career-recommender/frontend     # Mac/Linux

uv run streamlit run app.py
```

**Expected output:**

```
  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.x.x:8501
```

**Browser will auto-open!** If not, go to `http://localhost:8501`

### Step 9: Use the App!

1. **Homepage:** You'll see the AI Career Mentor homepage
2. **Click "Create New Account"**
   - Username: `krishna` (or anything)
   - Email: `krishna@example.com`
   - Password: `mypass123`
   - Click "Create Account"
3. **Login Page:** Use the credentials you just created
4. **Main App:**
   - Upload your resume (PDF or TXT) in the left sidebar
   - Go to "Career Roadmap" tab → See your personalized roadmap
   - Go to "Growth Analytics" tab → See your skills chart
   - Go to "Chat & Mentor" tab → Ask career questions!

**Try asking:**

- "What skills should I focus on to become a senior developer?"
- "What's the salary range for data scientists in the US?"
- "Create a learning plan for me to switch to machine learning"

The AI will reference your resume and past conversations!

---

## 🔧 Troubleshooting Common Issues

### "psql: command not found"

**Problem:** PostgreSQL bin folder not in PATH.

**Fix:**

- **Windows:** Add `C:\Program Files\PostgreSQL\18\bin` to System PATH
  - Search "Environment Variables" → Edit System Variables → Path → New → Add path → OK
  - Restart terminal
- **Mac/Linux:** Usually auto-installed, try `sudo apt install postgresql` (Linux) or `brew install postgresql` (Mac)

### "Connection refused" on port 8000 or 8501

**Problem:** Backend/Frontend not running.

**Fix:** Make sure both terminals are running:

- Terminal 1: `uvicorn app.main:app --reload` (backend)
- Terminal 2: `streamlit run app.py` (frontend)

### "401 Unauthorized" when logging in

**Problem:** Password mismatch or user doesn't exist.

**Fix:**

- Run `uv run python seed_db.py` to create test user
- Try: `testuser` / `password123`
- If registering new user, make sure password is at least 6 characters

### "OpenAI API Error: Invalid API Key"

**Problem:** OpenAI key not set or invalid.

**Fix:**

- Check `.env` file
- Make sure `OPENAI_API_KEY` starts with `sk-`
- Verify key is active on platform.openai.com
- Restart backend server after changing `.env`

### "No resume found for user"

**Problem:** Resume not uploaded yet.

**Fix:**

- Upload resume in left sidebar first
- Wait for "Resume uploaded successfully" message
- Then try Career Roadmap / Analytics

### ChromaDB "Collection not found" error

**Problem:** ChromaDB folder deleted or corrupted.

**Fix:**

```bash
# In project root
rm -rf data/chroma_db  # Mac/Linux
Remove-Item data\chroma_db -Recurse -Force  # Windows PowerShell

# Restart backend
```

### "Port 8000 already in use"

**Problem:** Another process using port 8000.

**Fix:**

```bash
# Windows: Find and kill process
netstat -ano | findstr :8000
taskkill /F /PID <PID>

# Mac/Linux
lsof -ti:8000 | xargs kill -9

# Or change port
uvicorn app.main:app --reload --port 8001
# And update frontend API_URL in components/*.py to http://localhost:8001
```

---

## 📚 How to Customize This Project

### Change AI Model

In `backend/app/services/openai_service.py`:

```python
# Line 9
llm = ChatOpenAI(temperature=0.3, model_name="gpt-4o-mini", ...)

# Change to:
llm = ChatOpenAI(temperature=0.3, model_name="gpt-4", ...)  # More powerful
```

### Adjust Session Limit (currently 10)

In `backend/app/crud.py`, line 20:

```python
if session_count >= 10:  # Change 10 to any number
```

### Customize AI Personality

In `backend/app/services/openai_service.py`, `generate_chat_response()` function:

```python
prompt_template = """
You are a Personal AI Career Mentor...  # Edit this!
```

Change the prompt to make the AI:

- Stricter/more formal
- Funny/casual
- Focused on specific industries
- etc.

### Add More Resource Types

In `backend/app/services/openai_service.py`, `generate_roadmap()` function:

```python
- type (string: "course", "article", "video", "book", or "tool")

# Add: "podcast", "workshop", "certification", etc.
```

### Change Theme/Colors

Streamlit doesn't have easy theming. Options:

- Create `.streamlit/config.toml` in frontend folder:
  ```toml
  [theme]
  primaryColor = "#ff4b4b"
  backgroundColor = "#0e1117"
  secondaryBackgroundColor = "#262730"
  textColor = "#fafafa"
  ```
- Or use custom CSS in `app.py`:
  ```python
  st.markdown("<style>...</style>", unsafe_allow_html=True)
  ```

---

## 🎓 Learning Resources (If You Want to Understand the Code Better)

### FastAPI

- Official Tutorial: https://fastapi.tiangolo.com/tutorial/
- Why I use it: Fast, automatic API docs, modern Python

### Streamlit

- Docs: https://docs.streamlit.io/
- Why I use it: Easiest way to build data apps in Python

### SQLAlchemy

- Docs: https://docs.sqlalchemy.org/
- Why I use it: Best Python ORM, handles relationships well

### LangChain

- Docs: https://python.langchain.com/docs/get_started/introduction
- Why I use it: Simplifies OpenAI API calls, great for prompts

### ChromaDB

- Docs: https://docs.trychroma.com/
- Why I use it: Easy vector database, built-in embeddings

### PostgreSQL

- Tutorial: https://www.postgresqltutorial.com/
- Why I use it: Reliable, scalable, free, industry standard

---

## 🤝 Project Philosophy (Why I Built It This Way)

1. **Separation of Concerns:** Backend handles logic, frontend handles display. You can swap Streamlit for React later without touching backend code.

2. **Modularity:** Each file has ONE job. `auth.py` only handles authentication, `chat.py` only handles chat, etc. Easy to debug and extend.

3. **DRY (Don't Repeat Yourself):** CRUD operations in one file, not scattered. Reusable components in frontend.

4. **Security:** Passwords hashed, no plain text. Could add JWT tokens for production.

5. **Scalability:** PostgreSQL handles millions of rows. ChromaDB handles large embeddings. FastAPI is async (handles many users).

6. **User Experience:** Session numbers per-user (not confusing global IDs), cross-session memory (AI remembers everything), progress tracking (visual feedback).

7. **Simplicity:** No unnecessary complexity. Could use Kubernetes, microservices, etc., but for a personal project, this is perfect.

---

## 🚀 Next Steps (Ideas to Extend This)

1. **Deploy to Cloud:**
   - Use Railway, Render, or Heroku for backend
   - Use Streamlit Cloud for frontend
   - Managed PostgreSQL (ElephantSQL, Supabase)

2. **Add JWT Authentication:**
   - Return token on login
   - Require token for all API calls
   - Store in `localStorage` on frontend

3. **Real-time Chat:**
   - Use WebSockets instead of HTTP
   - Streaming responses (like ChatGPT)

4. **Email Notifications:**
   - Send roadmap completion reminders
   - Weekly progress reports

5. **Social Features:**
   - Share roadmaps with friends
   - Public career paths leaderboard

6. **Multi-Language Support:**
   - Internationalization (i18n)
   - Detect user language, translate UI

7. **Voice Input:**
   - Use Whisper API for speech-to-text
   - Ask questions by voice

8. **Mobile App:**
   - Build React Native frontend
   - Same backend API

---

## 📝 License & Usage

This project was created by **Krishna Nand Pathak** as a personal learning project. Feel free to:

- Use it for personal career guidance
- Learn from the code
- Modify and extend it
- Share with friends

**Please don't:**

- Sell it without permission
- Remove my name from credits
- Use it for malicious purposes

---

## 🙏 Acknowledgments

- **OpenAI** for GPT-4o-mini and embeddings API
- **Streamlit** team for making UI development easy
- **FastAPI** team for a phenomenal framework
- **Chroma** team for the elegant vector database

---

## 📬 Contact

**Developer:** Krishna Nand Pathak

---

## 🎉 Final Words

Building this project taught me a lot about:

- Full-stack development
- AI integration
- Database design
- User experience
- System architecture

I hope this README helps you understand every aspect of the project. Whether you're a beginner learning to code or an experienced developer evaluating the architecture, I tried to explain things in a way that makes sense to everyone.

If you found this useful, give me a shout! If you found bugs, let me know. If you built something cool with this, I'd love to see it!

Happy coding! 🚀

--- Hrudai deepak Bonagiri
