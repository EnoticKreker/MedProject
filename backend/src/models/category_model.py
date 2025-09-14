from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.models.question_category_model import question_categories
from .base_model import Base


class CategoryModel(Base):
    __tablename__ = "categories"

    name: Mapped[str] = mapped_column(String(50), unique=True)

    questions = relationship(
        "QuestionModel",
        secondary=question_categories,
        back_populates="categories",
        lazy="selectin"
    )