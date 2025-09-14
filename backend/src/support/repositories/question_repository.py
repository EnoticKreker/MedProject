from fastapi import HTTPException
from sqlalchemy import delete, distinct, func, select, update
from sqlalchemy.orm import load_only
from typing import List, Optional

from src.models.category_model import CategoryModel
from src.support.schemas.validator_schema import ValidationResult
from src.repositories.sqlalchemy_repository import SqlAlchemyRepository, ModelType
from src.models.question_model import QuestionModel
from src.config.database.db_helper import db_helper

from src.support.validator.questions_validator import QuestionValidator
from src.config.project_config import settings

from ..schemas.question_schema import QuestionRead

import io
import pandas as pd


class QuestionRepository(SqlAlchemyRepository[ModelType, QuestionRead, None]):
    
    async def clear_all(self):
        async with self._session_factory() as session:
            async with session.begin():
                await session.execute(delete(self.model))

    async def filter(
        self,
        fields: List[str] | None = None,
        order: List[str] | None = None,
        limit: int = 100,
        offset: int = 0,
        category_ids: Optional[List[int]] = None,
        agreement_filter: Optional[bool] = None
    ) -> List[ModelType] | None:
        async with self._session_factory() as session:
            stmt = select(self.model)
            if fields:
                model_fields = [getattr(self.model, field) for field in fields]
                stmt = stmt.options(load_only(*model_fields))
            if category_ids:
                stmt = stmt.join(self.model.categories).filter(
                    CategoryModel.id.in_(category_ids)
                )
                
            if agreement_filter == "true":
                stmt = stmt.filter(self.model.agreement.is_(True))
            elif agreement_filter == "false":
                stmt = stmt.filter((self.model.agreement.is_(False)) | (self.model.agreement.is_(None)))
            if order:
                stmt = stmt.order_by(*order)
            if limit is not None:
                stmt = stmt.limit(limit)
            if offset is not None:
                stmt = stmt.offset(offset)
                
            stmt = stmt.distinct(self.model.id)

            row = await session.execute(stmt)
            return row.scalars().all()

    async def all(self) -> List[ModelType] | None:
        return await self.filter()
    
    async def count(self, category_ids: Optional[List[int]] = None, agreement_filter: Optional[bool] = None) -> int:
        async with self._session_factory() as session:
            stmt = select(func.count(distinct(self.model.id)))
            if category_ids:
                stmt = stmt.join(self.model.categories).filter(
                    CategoryModel.id.in_(category_ids)
                )
            if agreement_filter == "true":
                stmt = stmt.filter(self.model.agreement.is_(True))
            elif agreement_filter == "false":
                stmt = stmt.filter((self.model.agreement.is_(False)) | (self.model.agreement.is_(None)))

            return await session.scalar(stmt)
    
    async def find_by_id(self, id: int) -> ModelType | None:
        async with self._session_factory() as session:
            stmt = select(self.model).where(self.model.question_id == id)
            result = await session.execute(stmt)
            return result.scalar_one_or_none()

    async def exists(self, **filters) -> bool:
        stmt = select(self.model).filter_by(**filters)
        async with self._session_factory() as session:
            result = await session.execute(stmt)
            return result.scalar() is not None

    async def upload(self, file_bytes: bytes) -> ValidationResult:
        if len(file_bytes) > settings.MAX_FILE_SIZE:
            raise HTTPException(
                status_code=400,
                detail=f"Файл слишком большой. Максимальный размер: {settings.MAX_FILE_SIZE / 1024 / 1024} МБ",
            )
        
        df = pd.read_excel(io.BytesIO(file_bytes), engine='openpyxl')
        model_columns = self.model.__table__.columns.keys()
        df = df[[c for c in df.columns if c in model_columns]]
        records = df.to_dict(orient="records")
        
        question_validator = QuestionValidator(repository=self)
        validation_result = await question_validator.validate_rows(records)
        
        if validation_result.errors:
            validation_result.inserted_count = 0
            return validation_result
        
        await self.clear_all()

        async with self._session_factory() as session:
            objects = [self.model(**r) for r in records]
            session.add_all(objects)
            await session.commit()

        validation_result.inserted_count = len(objects)
        return validation_result


    async def update_agreement(self, id: int, agreement: bool) -> bool:
        async with self._session_factory() as session:
            stmt = (
                update(self.model)
                .where(self.model.question_id == id)
                .values(agreement=agreement)
                .execution_options(synchronize_session="fetch")
            )
            
            result = await session.execute(stmt)
            await session.commit()
            return result.rowcount > 0
        
    async def add_categories_questions(self, question_id: int, category_ids: list[int]):
        async with self._session_factory() as session:
            stmt = select(QuestionModel).where(QuestionModel.question_id == question_id)
            result = await session.execute(stmt)
            question = result.scalar_one_or_none()
            if not question:
                raise HTTPException(
                    status_code=404,
                    detail=f"Вопрос не найден. Добавление категории невозможно.",
                )
                
            stmt = select(CategoryModel).where(CategoryModel.id.in_(category_ids))
            categories = (await session.execute(stmt)).scalars().all()
            if not question:
                raise HTTPException(
                    status_code=404,
                    detail=f"Каттегория не найдена. Добавление категории невозможно.",
                )
            
            
            existing_category_ids = {cat.id for cat in question.categories}
            for category in categories:
                if category.id not in existing_category_ids:
                    question.categories.append(category)
            await session.commit()
            await session.refresh(question)
            return question

question_repository = QuestionRepository(
    model=QuestionModel,
    db_session=db_helper.get_db_session
)
