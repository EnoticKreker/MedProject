from datetime import datetime
from sqlalchemy import Boolean, DateTime, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base_model import Base
from src.models.question_category_model import question_categories


class QuestionModel(Base):
    __tablename__ = "questions"
    
    question_id: Mapped[int | None] = mapped_column(index=True, unique=True)
    
    hospital_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    device_type: Mapped[str | None] = mapped_column(String(100), nullable=True)
    user_login: Mapped[str | None] = mapped_column(String(100), nullable=True)
    
    question_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    question_date: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    answer_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    
    agreement: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    
    categories = relationship(
        "CategoryModel",
        secondary=question_categories,
        back_populates="questions",
        lazy="selectin"
    )