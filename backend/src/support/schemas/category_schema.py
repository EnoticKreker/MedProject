from pydantic import BaseModel


class CategoryBase(BaseModel):
    name: str
    
    class Config:
        from_attributes = True


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(CategoryBase):
    pass


class CategoryResponse(CategoryBase):
    id: int
    
    class Config:
        from_attributes = True


class CategoryListResponse(BaseModel):
    id: int | None = None
    name: str | None = None
