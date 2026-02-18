from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    pass

class UserRegister(BaseModel):
    username: str
    email: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class User(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class ChatMessageBase(BaseModel):
    role: str
    content: str

class ChatMessageCreate(ChatMessageBase):
    session_id: int
    user_id: int

class ChatMessage(ChatMessageBase):
    id: int
    timestamp: datetime

    class Config:
        from_attributes = True

class ChatSessionBase(BaseModel):
    summary: Optional[str] = None
    resume_id: Optional[int] = None

class ChatSessionCreate(ChatSessionBase):
    user_id: int

class ChatSession(ChatSessionBase):
    id: int
    session_number: Optional[int] = None
    created_at: datetime
    messages: List[ChatMessage] = []

    class Config:
        from_attributes = True

class ResumeBase(BaseModel):
    parsed_content: str

class ResumeCreate(ResumeBase):
    user_id: int
    file_path: str

class Resume(ResumeBase):
    id: int
    uploaded_at: datetime

    class Config:
        from_attributes = True

class CareerRecommendationBase(BaseModel):
    career_name: str
    reasoning: str
    salary_range: str

class CareerRecommendationCreate(CareerRecommendationBase):
    user_id: int

class CareerRecommendation(CareerRecommendationBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
