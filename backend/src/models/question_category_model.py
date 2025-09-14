# src/models/question_category_table.py
from sqlalchemy import Table, Column, ForeignKey
from src.models.base_model import Base

question_categories = Table(
    "question_categories",
    Base.metadata,
    Column("question_id", ForeignKey("questions.id", ondelete="CASCADE"), primary_key=True),
    Column("category_id", ForeignKey("categories.id", ondelete="CASCADE"), primary_key=True),
)
