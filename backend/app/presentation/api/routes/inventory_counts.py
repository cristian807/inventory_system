from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from app.infrastructure.persistence.database import get_db
from app.infrastructure.persistence.repositories import (
    InventoryRepository,
    ProductRepository,
    WarehouseRepository
)
from app.application.dtos.dtos import (
    InventoryCountCreateDTO,
    InventoryCountResponseDTO,
    InventoryCountDetailDTO,
    InventoryItemCreateDTO,
    InventoryItemResponseDTO
)
from app.application.use_cases.inventory_count_use_cases import (
    CreateInventoryCountUseCase,
    GetInventoryCountsUseCase,
    GetInventoryCountDetailUseCase,
    CloseInventoryCountUseCase,
    AddItemToCountUseCase
)
from app.infrastructure.security import get_current_user, require_admin

router = APIRouter(prefix="/api/inventory-counts", tags=["inventory-counts"])


@router.post("/", response_model=InventoryCountResponseDTO, status_code=status.HTTP_201_CREATED)
async def create_inventory_count(
    dto: InventoryCountCreateDTO,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    from app.infrastructure.persistence.models import UserRole
    
    # Si es USER, validar que tenga acceso a la bodega
    if current_user.role == UserRole.USER:
        user_warehouse_ids = [w.id for w in current_user.assigned_warehouses]
        if dto.warehouse_id not in user_warehouse_ids:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"No tiene permisos para crear conteos en la bodega {dto.warehouse_id}"
            )
    
    try:
        use_case = CreateInventoryCountUseCase(
            InventoryRepository(db),
            WarehouseRepository(db)
        )
        result = await use_case.execute(dto, current_user.id)
        return result
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/", response_model=List[InventoryCountResponseDTO])
async def get_inventory_counts(
    warehouse_id: Optional[int] = None,
    status: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    from app.infrastructure.persistence.models import UserRole
    
    # Si es USER, solo mostrar conteos de sus bodegas asignadas
    if current_user.role == UserRole.USER:
        user_warehouse_ids = [w.id for w in current_user.assigned_warehouses]
        if warehouse_id and warehouse_id not in user_warehouse_ids:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tiene permisos para ver conteos de esa bodega"
            )
        if not warehouse_id and user_warehouse_ids:
            pass
    
    try:
        use_case = GetInventoryCountsUseCase(InventoryRepository(db))
        result = await use_case.execute(warehouse_id=warehouse_id, status=status)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/{count_id}", response_model=InventoryCountDetailDTO)
async def get_inventory_count_detail(
    count_id: int,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    try:
        use_case = GetInventoryCountDetailUseCase(InventoryRepository(db))
        result = await use_case.execute(count_id)
        
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Conteo con ID {count_id} no encontrado"
            )
        
        from app.infrastructure.persistence.models import UserRole
        if current_user.role == UserRole.USER:
            user_warehouse_ids = [w.id for w in current_user.assigned_warehouses]
            if result.warehouse_id not in user_warehouse_ids:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="No tiene permisos para ver este conteo"
                )
        
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.put("/{count_id}/close", response_model=InventoryCountResponseDTO)
async def close_inventory_count(
    count_id: int,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_admin)
):
    """
    Cerrar un conteo de inventario.
    Requiere rol ADMIN.
    """
    try:
        use_case = CloseInventoryCountUseCase(InventoryRepository(db))
        result = await use_case.execute(count_id)
        return result
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post("/{count_id}/items", response_model=InventoryItemResponseDTO, status_code=status.HTTP_201_CREATED)
async def add_item_to_count(
    count_id: int,
    dto: InventoryItemCreateDTO,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Agregar un item (producto) a un conteo de inventario.
    El sistema calcula automáticamente las unidades totales.
    """
    try:
        # Validar permisos: verificar que el usuario tenga acceso al conteo
        inventory_repo = InventoryRepository(db)
        count = await inventory_repo.get_count_by_id(count_id)
        
        if not count:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Conteo con ID {count_id} no encontrado"
            )
        
        from app.infrastructure.persistence.models import UserRole
        if current_user.role == UserRole.USER:
            user_warehouse_ids = [w.id for w in current_user.assigned_warehouses]
            if count.warehouse_id not in user_warehouse_ids:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="No tiene permisos para agregar items a este conteo"
                )
        
        use_case = AddItemToCountUseCase(
            inventory_repo,
            ProductRepository(db)
        )
        result = await use_case.execute(count_id, dto)
        return result
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/{count_id}/items", response_model=List[InventoryItemResponseDTO])
async def get_count_items(
    count_id: int,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Obtener todos los items de un conteo específico.
    """
    try:
        use_case = GetInventoryCountDetailUseCase(InventoryRepository(db))
        count_detail = await use_case.execute(count_id)
        
        if not count_detail:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Conteo con ID {count_id} no encontrado"
            )
        
        # Validar permisos
        from app.infrastructure.persistence.models import UserRole
        if current_user.role == UserRole.USER:
            user_warehouse_ids = [w.id for w in current_user.assigned_warehouses]
            if count_detail.warehouse_id not in user_warehouse_ids:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="No tiene permisos para ver items de este conteo"
                )
        
        return count_detail.items
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
