from src.repositories.sqlalchemy_repository import ModelType
from src.services.base_service import BaseService
from ..repositories.question_repository import question_repository
from fastapi import HTTPException, UploadFile, status
from typing import List, Optional


class QuestionService(BaseService):
    
    async def replace_data(self):
        await self.repository.clear_all()
    
    
    async def filter(
        self,
        fields: Optional[List[str]] = None,
        order: Optional[List[str]] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        category_ids: Optional[List[int]] = None,
        agreement_filter: Optional[bool] = None
    ) -> List[ModelType] | None:
        return await self.repository.filter(
            fields=fields,
            order=order,
            limit=limit,
            offset=offset,
            category_ids=category_ids,
            agreement_filter=agreement_filter
        )
        
    async def count(self, category_ids: Optional[List[int]] = None, agreement_filter: Optional[bool] = None) -> int:
        return await self.repository.count(category_ids=category_ids, agreement_filter=agreement_filter)

    async def exists(self, **filters) -> bool:
        return await self.repository.exists(**filters)
    
    async def find_by_id(self, id: int) -> dict:
        return await self.repository.find_by_id(id)

    async def upload_excel(self, file: UploadFile) -> dict:
        return await self.upload(file)
    
    async def set_agreement(self, id: int, agreement: bool) -> dict:
        updated = await self.repository.update_agreement(id, agreement)
        if not updated:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Вопрос не найден"
            )
        return {"success": True, "id": id, "agreement": agreement}
    
    async def add_categories_questions(self, question_id: int, category_ids: list[int]):
        return await self.repository.add_categories_questions(question_id, category_ids)
    
    async def all(self) -> list:
        return await self.repository.all()


# Экземпляр сервиса
question_service = QuestionService(repository=question_repository)
