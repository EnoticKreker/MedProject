from typing import List, Optional
from fastapi import APIRouter, Query, UploadFile, Depends, HTTPException, status
from src.support.services.questions_service import question_service
from src.support.schemas.question_schema import QuestionCategory, QuestionRead, QuestionUpdateAgreement

router = APIRouter(
    prefix="/questions", tags=["questions"]
)

@router.post("/upload/")
async def upload_questions(file: UploadFile):
    if not file.filename.endswith(".xlsx"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Только файлы .xlsx поддерживаются"
        )

    try:
        result = await question_service.upload_excel(file)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при загрузке файла: {str(e)}"
        )


@router.get("/")
async def get_questions(page: int = 1, limit: int = 20, category_ids: Optional[List[int]] = Query(None), agreement_filter: str | None = Query(default="all")):
    offset = (page - 1) * limit
    questions = await question_service.filter(limit=limit, offset=offset, category_ids=category_ids, agreement_filter=agreement_filter)
    total = await question_service.count(category_ids=category_ids, agreement_filter=agreement_filter)
    return {
        "items": questions,
        "total": total
    }

@router.get("/{question_id}", response_model=QuestionRead)
async def get_question(question_id: int):
    question = await question_service.find_by_id(question_id)
    if not question:
        raise HTTPException(status_code=404, detail="Вопрос не найден.")
    return question

@router.patch("/{id}/agreement")
async def update_agreement(id: int, data: QuestionUpdateAgreement):
    result = await question_service.set_agreement(id, data.agreement)
    if not result["success"]:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Вопрос не найден"
        )
    return result


@router.post("/{question_id}/categories", response_model=QuestionRead)
async def assign_categories_to_question(question_id: int, data: QuestionCategory):
    try:
        question = await question_service.add_categories_questions(
            question_id=question_id,
            category_ids=data.category_ids,
        )
        return question
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при добавлении категорий: {str(e)}"
        )