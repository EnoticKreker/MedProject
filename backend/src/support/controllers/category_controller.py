from typing import Annotated

from fastapi import Depends, HTTPException, Query, APIRouter, status
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_204_NO_CONTENT

from ..schemas.category_schema import (
    CategoryCreate,
    CategoryResponse,
    CategoryListResponse
)
from ..services.category_service import category_service

router = APIRouter(prefix="/category", tags=["category"])


@router.get("/exists")
async def exists_category_for_name(name: str) -> bool:
    try:
        return await category_service.exists(name)
    except Exception as e:
        raise HTTPException(HTTP_400_BAD_REQUEST, str(e))


@router.post("/")
async def create_category(
        data: CategoryCreate,
) -> CategoryResponse:
    try:
        return await category_service.create(model=data)
    except Exception as e:
        raise HTTPException(HTTP_400_BAD_REQUEST, str(e))


@router.put("/{pk}")
async def update_category(pk: int, data: CategoryCreate) -> CategoryResponse:
    try:
        return await category_service.update(pk=pk, model=data)
    except Exception as e:
        raise HTTPException(HTTP_400_BAD_REQUEST, str(e))


@router.delete("/{pk}", status_code=HTTP_204_NO_CONTENT)
async def delete_category(pk: int):
    try:
        return await category_service.delete(pk=pk)
    except Exception as e:
        raise HTTPException(HTTP_400_BAD_REQUEST, str(e))


@router.get("/{pk}")
async def get_single_category(pk: int) -> CategoryResponse:
    try:
        result = await category_service.get(pk=pk)
        print(result)
        if result is None:
            raise HTTPException(status_code=404, detail="Категория не найдена.")
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Ошибка при получении категории: {str(e)}"
        )


@router.get("/")
async def filter_category(
        fields: Annotated[list, Query()] = [],
        order: Annotated[list, Query()] = [],
        limit: int | None = None,
        offset: int | None = None
) -> list[CategoryListResponse] | None:
    try:
        return await category_service.filter(
            fields=fields,
            order=order,
            limit=limit,
            offset=offset
        )
    except Exception as e:
        raise HTTPException(HTTP_400_BAD_REQUEST, str(e))
