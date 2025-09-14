from pydantic import BaseModel
from typing import List


class ValidationResult(BaseModel):
    errors: List[str] = []
    warnings: List[str] = []
    inserted_count: int = 0
