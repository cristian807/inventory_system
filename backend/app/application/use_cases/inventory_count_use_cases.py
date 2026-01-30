from typing import List, Optional
from datetime import datetime, date
from app.domain.repositories.repository_interfaces import IInventoryRepository, IWarehouseRepository, IUserRepository, IProductRepository
from app.application.dtos.dtos import (
    InventoryCountCreateDTO, 
    InventoryCountResponseDTO,
    InventoryCountDetailDTO,
    InventoryItemCreateDTO,
    InventoryItemResponseDTO
)
from app.infrastructure.persistence.models import InventoryCountModel, InventoryCountStatus, InventoryItemModel


class CreateInventoryCountUseCase:

    def __init__(self, inventory_repo: IInventoryRepository, warehouse_repo: IWarehouseRepository):
        self.inventory_repo = inventory_repo
        self.warehouse_repo = warehouse_repo
    
    async def execute(self, dto: InventoryCountCreateDTO, user_id: int) -> InventoryCountResponseDTO:
        # Verificar que la bodega existe
        warehouse = await self.warehouse_repo.get_by_id(dto.warehouse_id)
        if not warehouse:
            raise ValueError(f"Bodega con ID {dto.warehouse_id} no encontrada")
        
        # Crear el conteo
        count_model = InventoryCountModel(
            name=dto.name,
            cut_off_date=datetime.strptime(dto.cut_off_date, "%Y-%m-%d").date(),
            warehouse_id=dto.warehouse_id,
            status=InventoryCountStatus.IN_PROGRESS,
            created_by=user_id
        )
        
        created_count = await self.inventory_repo.create_count(count_model)
        
        return InventoryCountResponseDTO(
            id=created_count.id,
            name=created_count.name,
            cut_off_date=created_count.cut_off_date.isoformat(),
            warehouse_id=created_count.warehouse_id,
            warehouse_name=warehouse.name,
            status=created_count.status.value,
            created_by=created_count.created_by,
            created_at=created_count.created_at,
            closed_at=created_count.closed_at,
            items_count=0
        )


class GetInventoryCountsUseCase:

    def __init__(self, inventory_repo: IInventoryRepository):
        self.inventory_repo = inventory_repo
    
    async def execute(self, warehouse_id: Optional[int] = None, status: Optional[str] = None) -> List[InventoryCountResponseDTO]:
        counts = await self.inventory_repo.get_counts(warehouse_id=warehouse_id, status=status)
        
        result = []
        for count in counts:
            items_count = len(count.items) if hasattr(count, 'items') and count.items else 0
            warehouse_name = count.warehouse.name if count.warehouse else None
            creator_username = count.creator.username if count.creator else None
            
            result.append(InventoryCountResponseDTO(
                id=count.id,
                name=count.name,
                cut_off_date=count.cut_off_date.isoformat(),
                warehouse_id=count.warehouse_id,
                warehouse_name=warehouse_name,
                status=count.status.value,
                created_by=count.created_by,
                creator_username=creator_username,
                created_at=count.created_at,
                closed_at=count.closed_at,
                items_count=items_count
            ))
        
        return result


class GetInventoryCountDetailUseCase:
    """Obtener detalle de un conteo con sus items"""
    
    def __init__(self, inventory_repo: IInventoryRepository):
        self.inventory_repo = inventory_repo
    
    async def execute(self, count_id: int) -> Optional[InventoryCountDetailDTO]:
        count = await self.inventory_repo.get_count_by_id(count_id)
        if not count:
            return None
        
        items = []
        if hasattr(count, 'items') and count.items:
            for item in count.items:
                items.append(InventoryItemResponseDTO(
                    id=item.id,
                    count_id=item.count_id,
                    warehouse_id=item.warehouse_id,
                    product_id=item.product_id,
                    packages_count=item.packages_count,
                    quantity=item.quantity,
                    created_at=item.created_at,
                    updated_at=item.updated_at
                ))
        
        return InventoryCountDetailDTO(
            id=count.id,
            name=count.name,
            cut_off_date=count.cut_off_date.isoformat(),
            warehouse_id=count.warehouse_id,
            warehouse_name=count.warehouse.name if count.warehouse else "",
            status=count.status.value,
            created_by=count.created_by,
            creator_username=count.creator.username if count.creator else "",
            created_at=count.created_at,
            closed_at=count.closed_at,
            items=items
        )


class CloseInventoryCountUseCase:
    """Cerrar un conteo de inventario"""
    
    def __init__(self, inventory_repo: IInventoryRepository):
        self.inventory_repo = inventory_repo
    
    async def execute(self, count_id: int) -> InventoryCountResponseDTO:
        count = await self.inventory_repo.get_count_by_id(count_id)
        if not count:
            raise ValueError(f"Conteo con ID {count_id} no encontrado")
        
        if count.status == InventoryCountStatus.CLOSED:
            raise ValueError("El conteo ya está cerrado")
        
        count.status = InventoryCountStatus.CLOSED
        count.closed_at = datetime.utcnow()
        
        updated_count = await self.inventory_repo.update_count(count)
        
        items_count = len(updated_count.items) if hasattr(updated_count, 'items') and updated_count.items else 0
        warehouse_name = updated_count.warehouse.name if updated_count.warehouse else None
        creator_username = updated_count.creator.username if updated_count.creator else None
        
        return InventoryCountResponseDTO(
            id=updated_count.id,
            name=updated_count.name,
            cut_off_date=updated_count.cut_off_date.isoformat(),
            warehouse_id=updated_count.warehouse_id,
            warehouse_name=warehouse_name,
            status=updated_count.status.value,
            created_by=updated_count.created_by,
            creator_username=creator_username,
            created_at=updated_count.created_at,
            closed_at=updated_count.closed_at,
            items_count=items_count
        )


class AddItemToCountUseCase:
    """Agregar un item a un conteo de inventario"""
    
    def __init__(self, inventory_repo: IInventoryRepository, product_repo: IProductRepository):
        self.inventory_repo = inventory_repo
        self.product_repo = product_repo
    
    async def execute(self, count_id: int, dto: InventoryItemCreateDTO) -> InventoryItemResponseDTO:
        # Verificar que el conteo existe y está abierto
        count = await self.inventory_repo.get_count_by_id(count_id)
        if not count:
            raise ValueError(f"Conteo con ID {count_id} no encontrado")
        
        if count.status == InventoryCountStatus.CLOSED:
            raise ValueError("No se pueden agregar items a un conteo cerrado")
        
        # Verificar que el producto existe
        product = await self.product_repo.get_by_id(dto.product_id)
        if not product:
            raise ValueError(f"Producto con ID {dto.product_id} no encontrado")
        
        # Calcular cantidad total en unidades
        calculated_quantity = dto.packages_count * product.units_per_package
        
        # Crear el item
        item_model = InventoryItemModel(
            count_id=count_id,
            warehouse_id=count.warehouse_id,  # Usar la bodega del conteo
            product_id=dto.product_id,
            packages_count=dto.packages_count,
            quantity=calculated_quantity
        )
        
        created_item = await self.inventory_repo.create(item_model)
        
        return InventoryItemResponseDTO(
            id=created_item.id,
            count_id=created_item.count_id,
            warehouse_id=created_item.warehouse_id,
            product_id=created_item.product_id,
            packages_count=created_item.packages_count,
            quantity=created_item.quantity,
            created_at=created_item.created_at,
            updated_at=created_item.updated_at
        )
