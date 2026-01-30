from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.persistence.database import get_db
from app.infrastructure.persistence.repositories import ProductRepository
from app.application.use_cases.product_use_cases import (
    CreateProductUseCase, GetProductByIdUseCase, GetAllProductsUseCase,
    UpdateProductUseCase, DeleteProductUseCase
)
from app.application.dtos.dtos import ProductCreateDTO, ProductResponseDTO
from app.infrastructure.security import get_current_user, require_admin
from typing import List

router = APIRouter(prefix="/api/products", tags=["products"])


@router.post("/", response_model=ProductResponseDTO)
async def create_product(
    product_dto: ProductCreateDTO, 
    session: AsyncSession = Depends(get_db),
    current_user = Depends(require_admin)
):
    repository = ProductRepository(session)
    use_case = CreateProductUseCase(repository)
    return await use_case.execute(product_dto)


@router.get("/", response_model=List[ProductResponseDTO])
async def get_all_products(
    skip: int = 0, 
    limit: int = 100, 
    session: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    repository = ProductRepository(session)
    use_case = GetAllProductsUseCase(repository)
    return await use_case.execute(skip, limit)


@router.get("/{product_id}", response_model=ProductResponseDTO)
async def get_product(
    product_id: int, 
    session: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    repository = ProductRepository(session)
    use_case = GetProductByIdUseCase(repository)
    product = await use_case.execute(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return product


@router.put("/{product_id}", response_model=ProductResponseDTO)
async def update_product(
    product_id: int, 
    product_dto: ProductCreateDTO, 
    session: AsyncSession = Depends(get_db),
    current_user = Depends(require_admin)
):
    repository = ProductRepository(session)
    use_case = UpdateProductUseCase(repository)
    return await use_case.execute(product_id, product_dto)


@router.delete("/{product_id}")
async def delete_product(
    product_id: int, 
    session: AsyncSession = Depends(get_db),
    current_user = Depends(require_admin)
):
    repository = ProductRepository(session)
    use_case = DeleteProductUseCase(repository)
    success = await use_case.execute(product_id)
    if not success:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return {"message": "Producto eliminado correctamente"}
