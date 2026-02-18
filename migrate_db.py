from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv

# Load env variables
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

def migrate():
    engine = create_engine(DATABASE_URL)
    with engine.connect() as conn:
        # Migration 1: Add resume_id to chat_sessions
        try:
            print("Attempting to add resume_id column to chat_sessions...")
            conn.execute(text("ALTER TABLE chat_sessions ADD COLUMN resume_id INTEGER REFERENCES resumes(id)"))
            conn.commit()
            print("Migration successful: Added resume_id to chat_sessions.")
        except Exception as e:
            conn.rollback()
            print(f"resume_id migration skipped (may already exist): {e}")
        
        # Migration 2: Add hashed_password to users
        try:
            print("Attempting to add hashed_password column to users...")
            conn.execute(text("ALTER TABLE users ADD COLUMN hashed_password VARCHAR"))
            conn.commit()
            print("Migration successful: Added hashed_password to users.")
        except Exception as e:
            conn.rollback()
            print(f"hashed_password migration skipped (may already exist): {e}")
        
        # Migration 3: Add session_number to chat_sessions
        try:
            print("Attempting to add session_number column to chat_sessions...")
            conn.execute(text("ALTER TABLE chat_sessions ADD COLUMN session_number INTEGER DEFAULT 1"))
            conn.commit()
            print("Migration successful: Added session_number to chat_sessions.")
        except Exception as e:
            conn.rollback()
            print(f"session_number migration skipped (may already exist): {e}")
        
        # Migration 3b: Backfill session_number for existing sessions per user
        try:
            print("Backfilling session_number for existing sessions...")
            conn.execute(text("""
                WITH numbered AS (
                    SELECT id, ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY created_at) AS rn
                    FROM chat_sessions
                )
                UPDATE chat_sessions
                SET session_number = numbered.rn
                FROM numbered
                WHERE chat_sessions.id = numbered.id
            """))
            conn.commit()
            print("Backfill successful: session_number updated for all existing sessions.")
        except Exception as e:
            conn.rollback()
            print(f"session_number backfill skipped: {e}")

if __name__ == "__main__":
    migrate()
