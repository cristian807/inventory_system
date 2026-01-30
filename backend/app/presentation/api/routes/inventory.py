from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.persistence.database import get_db
from app.infrastructure.persistence.repositories import (
    InventoryRepository,
    ProductRepository,
    WarehouseRepository
)
from app.application.dtos.dtos import (
    InventoryItemCreateDTO,
    InventoryItemResponseDTO,
    WarehouseInventoryDTO
)
from app.application.use_cases.inventory_use_cases import (
    AddInventoryItemUseCase,
    UpdateInventoryQuantityUseCase,
    GetWarehouseInventoryUseCase,
    GetProductQuantityUseCase,
    RemoveProductFromWarehouseUseCase,
    GetAllWarehouseInventoryUseCase
)
from app.infrastructure.security import get_current_user, require_admin

router = APIRouter(prefix="/api/inventory", tags=["inventory"])


@router.post("/", response_model=InventoryItemResponseDTO, status_code=status.HTTP_201_CREATED)
async def add_product_to_warehouse(
    dto: InventoryItemCreateDTO,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    from app.infrastructure.persistence.models import UserRole
    
    if current_user.role == UserRole.USER:
        # Verificar si el usuario tiene asignada la bodega
        user_warehouse_ids = [w.id for w in current_user.assigned_warehouses]
        if dto.warehouse_id not in user_warehouse_ids:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"No tiene permisos para registrar en la bodega {dto.warehouse_id}. Solo puede registrar en sus bodegas asignadas."
            )
    
    try:
        use_case = AddInventoryItemUseCase(
            InventoryRepository(db),
            ProductRepository(db),
            WarehouseRepository(db)
        )
        result = await use_case.execute(dto)
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


@router.put("/{inventory_id}", response_model=InventoryItemResponseDTO)
async def update_inventory_quantity(
    inventory_id: int,
    quantity: int,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    from app.infrastructure.persistence.models import UserRole
    
    if current_user.role == UserRole.USER:
        inventory_repo = InventoryRepository(db)
        item = await inventory_repo.get_by_id(inventory_id)
        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Item de inventario no encontrado"
            )
        
        user_warehouse_ids = [w.id for w in current_user.assigned_warehouses]
        if item.warehouse_id not in user_warehouse_ids:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"No tiene permisos para modificar inventario de la bodega {item.warehouse_id}"
            )
    
    try:
        use_case = UpdateInventoryQuantityUseCase(InventoryRepository(db))
        result = await use_case.execute(inventory_id, quantity)
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


@router.get("/warehouse/{warehouse_id}", response_model=WarehouseInventoryDTO)
async def get_warehouse_inventory(
    warehouse_id: int,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    try:
        use_case = GetWarehouseInventoryUseCase(
            InventoryRepository(db),
            WarehouseRepository(db),
            ProductRepository(db)
        )
        result = await use_case.execute(warehouse_id)
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


@router.get("/warehouse/{warehouse_id}/product/{product_id}")
async def get_product_quantity(
    warehouse_id: int,
    product_id: int,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    try:
        use_case = GetProductQuantityUseCase(InventoryRepository(db))
        quantity = await use_case.execute(warehouse_id, product_id)
        return {"warehouse_id": warehouse_id, "product_id": product_id, "quantity": quantity}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.delete("/{inventory_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_product_from_warehouse(
    inventory_id: int,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_admin)
):
    try:
        use_case = RemoveProductFromWarehouseUseCase(InventoryRepository(db))
        success = await use_case.execute(inventory_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Inventory item with id {inventory_id} not found"
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/", response_model=list[WarehouseInventoryDTO])
async def get_all_warehouses_inventory(
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    try:
        use_case = GetAllWarehouseInventoryUseCase(
            InventoryRepository(db),
            WarehouseRepository(db),
            ProductRepository(db)
        )
        result = await use_case.execute()
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
