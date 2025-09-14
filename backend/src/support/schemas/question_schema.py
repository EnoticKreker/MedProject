from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional
from src.support.schemas.category_schema import CategoryResponse
from src.schemas.base_schema import Base



class QuestionBaseId(BaseModel):
    id: int

class QuestionBase(Base, QuestionBaseId):
    question_id: Optional[int]
    hospital_name: Optional[str]
    device_type: Optional[str]
    user_login: Optional[str]
    question_text: Optional[str]
    question_date: Optional[datetime]
    answer_text: Optional[str]
    agreement: Optional[bool]
    
    class Config:
        from_attributes = True

class QuestionRead(QuestionBase):
    categories: Optional[List[CategoryResponse]] = []

    class Config:
        from_attributes = True
        
class QuestionCreate(BaseModel):
    question_id: Optional[int]
    hospital_name: Optional[str]
    device_type: Optional[str]
    user_login: Optional[str]
    question_text: Optional[str]
    question_date: Optional[datetime]
    answer_text: Optional[str]
    
    
class QuestionUpdateAgreement(BaseModel):
    agreement: bool
    
    class Config:
        from_attributes = True
    
class QuestionCategory(BaseModel):
    category_ids: List[int]
    
    class Config:
        from_attributes = True