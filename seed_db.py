from backend.app.database import SessionLocal, engine
from backend.app import models
from backend.app.auth import get_password_hash

def seed_data():
    db = SessionLocal()
    
    # Create tables if they don't exist (already done in main.py, but good to ensure)
    models.Base.metadata.create_all(bind=engine)
    
    # Check if user exists
    user = db.query(models.User).filter(models.User.id == 1).first()
    if not user:
        print("Creating default user...")
        user = models.User(
            username="testuser",
            email="test@example.com",
            hashed_password=get_password_hash("password123")
        )
        db.add(user)
        db.commit()
    elif not user.hashed_password:
        # Update existing user with a password
        print("Updating default user with password...")
        user.hashed_password = get_password_hash("password123")
        db.commit()
    
    # Check if session exists
    session = db.query(models.ChatSession).filter(models.ChatSession.id == 1).first()
    if not session:
        print("Creating default chat session...")
        session = models.ChatSession(user_id=user.id, summary="Initial Session")
        db.add(session)
        db.commit()
        
    print("Database seeded successfully!")
    print("Default login => username: testuser | password: password123")
    db.close()

if __name__ == "__main__":
    seed_data()
