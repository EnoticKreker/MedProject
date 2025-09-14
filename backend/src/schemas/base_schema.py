from datetime import datetime
from typing import NewType

from pydantic import BaseModel

PyModel = NewType("PyModel", BaseModel)


class Base(BaseModel):
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
