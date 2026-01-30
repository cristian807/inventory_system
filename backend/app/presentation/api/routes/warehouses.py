from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.persistence.database import get_db
from app.infrastructure.persistence.repositories import WarehouseRepository
from app.application.use_cases.warehouse_use_cases import (
    CreateWarehouseUseCase, GetWarehouseByIdUseCase, GetAllWarehousesUseCase,
    UpdateWarehouseUseCase, DeleteWarehouseUseCase
)
from app.application.dtos.dtos import WarehouseCreateDTO, WarehouseResponseDTO
from app.infrastructure.security import get_current_user, require_admin
from typing import List

router = APIRouter(prefix="/api/warehouses", tags=["warehouses"])


@router.post("/", response_model=WarehouseResponseDTO)
async def create_warehouse(
    warehouse_dto: WarehouseCreateDTO, 
    session: AsyncSession = Depends(get_db),
    current_user = Depends(require_admin)
):
    repository = WarehouseRepository(session)
    use_case = CreateWarehouseUseCase(repository)
    return await use_case.execute(warehouse_dto)


@router.get("/", response_model=List[WarehouseResponseDTO])
async def get_all_warehouses(
    skip: int = 0, 
    limit: int = 100, 
    session: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    repository = WarehouseRepository(session)
    use_case = GetAllWarehousesUseCase(repository)
    return await use_case.execute(skip, limit)


@router.get("/{warehouse_id}", response_model=WarehouseResponseDTO)
async def get_warehouse(
    warehouse_id: int, 
    session: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    repository = WarehouseRepository(session)
    use_case = GetWarehouseByIdUseCase(repository)
    warehouse = await use_case.execute(warehouse_id)
    if not warehouse:
        raise HTTPException(status_code=404, detail="Bodega no encontrada")
    return warehouse


@router.put("/{warehouse_id}", response_model=WarehouseResponseDTO)
async def update_warehouse(
    warehouse_id: int, 
    warehouse_dto: WarehouseCreateDTO, 
    session: AsyncSession = Depends(get_db),
    current_user = Depends(require_admin)
):
    repository = WarehouseRepository(session)
    use_case = UpdateWarehouseUseCase(repository)
    return await use_case.execute(warehouse_id, warehouse_dto)


@router.delete("/{warehouse_id}")
async def delete_warehouse(
    warehouse_id: int, 
    session: AsyncSession = Depends(get_db),
    current_user = Depends(require_admin)
):
    repository = WarehouseRepository(session)
    use_case = DeleteWarehouseUseCase(repository)
    success = await use_case.execute(warehouse_id)
    if not success:
        raise HTTPException(status_code=404, detail="Bodega no encontrada")
    return {"message": "Bodega eliminada correctamente"}
