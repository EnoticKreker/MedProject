from typing import List
from src.support.schemas.question_schema import QuestionCreate
from src.support.schemas.validator_schema import ValidationResult


class QuestionValidator:
    def __init__(self, repository=None):
        self.repository = repository

    async def validate_rows(self, rows: List[dict]) -> ValidationResult:
        errors = []
        warnings = []

        # проверка на обязательные колонки
        required_fields = {"question_id", "question_text", "answer_text"}
        for field in required_fields:
            if any(field not in row for row in rows):
                errors.append(f"Отсутствует поле: {field}")

        seen_ids = set()
        for i, row in enumerate(rows, start=1):
            try:
                q = QuestionCreate(**row)  # проверка через Pydantic
            except Exception as e:
                errors.append(f"Строка {i}: {str(e)}")
                continue

            # проверка на дубликаты в файле
            if q.question_id in seen_ids:
                errors.append(f"Строка {i}: Дублирование question_id {q.question_id} в файле.")
            seen_ids.add(q.question_id)
            
        return ValidationResult(errors=errors, warnings=warnings)
