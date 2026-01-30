"""
Use cases para la gestión del inventario
"""
from typing import List
from app.domain.entities.entities import InventoryItem, Product, Warehouse
from app.domain.repositories.repository_interfaces import (
    IInventoryRepository,
    IProductRepository,
    IWarehouseRepository
)
from app.application.dtos.dtos import (
    InventoryItemCreateDTO,
    InventoryItemResponseDTO,
    InventoryDetailDTO,
    WarehouseInventoryDTO
)


class AddInventoryItemUseCase:
    """Use case para agregar un producto a una bodega"""
    
    def __init__(
        self,
        inventory_repo: IInventoryRepository,
        product_repo: IProductRepository,
        warehouse_repo: IWarehouseRepository
    ):
        self.inventory_repo = inventory_repo
        self.product_repo = product_repo
        self.warehouse_repo = warehouse_repo
    
    async def execute(self, dto: InventoryItemCreateDTO) -> InventoryItemResponseDTO:
        # Validar que el producto existe
        product = await self.product_repo.get_by_id(dto.product_id)
        if not product:
            raise ValueError(f"Product with id {dto.product_id} not found")
        
        # Validar que la bodega existe
        warehouse = await self.warehouse_repo.get_by_id(dto.warehouse_id)
        if not warehouse:
            raise ValueError(f"Warehouse with id {dto.warehouse_id} not found")
        
        # Calcular cantidad total en unidades
        calculated_quantity = dto.packages_count * product.units_per_package
        
        # Verificar si ya existe un registro para este producto-bodega (sin count_id)
        existing = await self.inventory_repo.get_by_warehouse_and_product(
            dto.warehouse_id, dto.product_id
        )
        
        if existing and not dto.count_id:
            # Si existe y no es parte de un conteo, actualizar la cantidad
            existing.quantity += calculated_quantity
            result = await self.inventory_repo.update(existing.id, existing)
        else:
            # Crear nuevo item (ya sea parte de conteo o independiente)
            from app.infrastructure.persistence.models import InventoryItemModel
            inventory_model = InventoryItemModel(
                count_id=dto.count_id,
                warehouse_id=dto.warehouse_id,
                product_id=dto.product_id,
                packages_count=dto.packages_count,
                quantity=calculated_quantity
            )
            result = await self.inventory_repo.create(inventory_model)
        
        return InventoryItemResponseDTO(
            id=result.id,
            count_id=result.count_id if hasattr(result, 'count_id') else None,
            warehouse_id=result.warehouse_id,
            product_id=result.product_id,
            packages_count=result.packages_count if hasattr(result, 'packages_count') else 0,
            quantity=result.quantity,
            created_at=result.created_at,
            updated_at=result.updated_at
        )


class UpdateInventoryQuantityUseCase:
    """Use case para actualizar la cantidad de un producto en una bodega"""
    
    def __init__(self, inventory_repo: IInventoryRepository):
        self.inventory_repo = inventory_repo
    
    async def execute(self, inventory_id: int, quantity: int) -> InventoryItemResponseDTO:
        if quantity <= 0:
            raise ValueError("Quantity must be greater than 0")
        
        # Obtener el item existente
        result = await self.inventory_repo.get_all()
        inventory_item = next((item for item in result if item.id == inventory_id), None)
        
        if not inventory_item:
            raise ValueError(f"Inventory item with id {inventory_id} not found")
        
        # Actualizar la cantidad
        inventory_item.quantity = quantity
        updated = await self.inventory_repo.update(inventory_id, inventory_item)
        
        return InventoryItemResponseDTO(
            id=updated.id,
            warehouse_id=updated.warehouse_id,
            product_id=updated.product_id,
            quantity=updated.quantity,
            created_at=updated.created_at,
            updated_at=updated.updated_at
        )


class GetWarehouseInventoryUseCase:
    """Use case para obtener el inventario completo de una bodega con detalles de productos"""
    
    def __init__(
        self,
        inventory_repo: IInventoryRepository,
        warehouse_repo: IWarehouseRepository,
        product_repo: IProductRepository
    ):
        self.inventory_repo = inventory_repo
        self.warehouse_repo = warehouse_repo
        self.product_repo = product_repo
    
    async def execute(self, warehouse_id: int) -> WarehouseInventoryDTO:
        # Validar que la bodega existe
        warehouse = await self.warehouse_repo.get_by_id(warehouse_id)
        if not warehouse:
            raise ValueError(f"Warehouse with id {warehouse_id} not found")
        
        # Obtener todos los items de inventario para la bodega
        inventory_items = await self.inventory_repo.get_by_warehouse(warehouse_id)
        
        # Enriquecer con detalles del producto
        items_detail = []
        total_products = 0
        
        for item in inventory_items:
            product = await self.product_repo.get_by_id(item.product_id)
            if product:
                items_detail.append(
                    InventoryDetailDTO(
                        id=item.id,
                        product_id=item.product_id,
                        product_name=product.name,
                        product_price=product.price,
                        quantity=item.quantity
                    )
                )
                total_products += item.quantity
        
        return WarehouseInventoryDTO(
            warehouse_id=warehouse.id,
            warehouse_name=warehouse.name,
            warehouse_location=warehouse.location,
            total_products_count=total_products,
            items=items_detail
        )


class GetProductQuantityUseCase:
    """Use case para obtener la cantidad de un producto específico en una bodega"""
    
    def __init__(self, inventory_repo: IInventoryRepository):
        self.inventory_repo = inventory_repo
    
    async def execute(self, warehouse_id: int, product_id: int) -> int:
        item = await self.inventory_repo.get_by_warehouse_and_product(warehouse_id, product_id)
        if item:
            return item.quantity
        return 0


class RemoveProductFromWarehouseUseCase:
    """Use case para remover un producto de una bodega"""
    
    def __init__(self, inventory_repo: IInventoryRepository):
        self.inventory_repo = inventory_repo
    
    async def execute(self, inventory_id: int) -> bool:
        return await self.inventory_repo.delete(inventory_id)


class GetAllWarehouseInventoryUseCase:
    """Use case para obtener el inventario de todas las bodegas"""
    
    def __init__(
        self,
        inventory_repo: IInventoryRepository,
        warehouse_repo: IWarehouseRepository,
        product_repo: IProductRepository
    ):
        self.inventory_repo = inventory_repo
        self.warehouse_repo = warehouse_repo
        self.product_repo = product_repo
    
    async def execute(self) -> List[WarehouseInventoryDTO]:
        # Obtener todas las bodegas
        warehouses = await self.warehouse_repo.get_all()
        
        result = []
        for warehouse in warehouses:
            # Para cada bodega, obtener su inventario
            inventory_items = await self.inventory_repo.get_by_warehouse(warehouse.id)
            
            items_detail = []
            total_products = 0
            
            for item in inventory_items:
                product = await self.product_repo.get_by_id(item.product_id)
                if product:
                    items_detail.append(
                        InventoryDetailDTO(
                            id=item.id,
                            product_id=item.product_id,
                            product_name=product.name,
                            product_price=product.price,
                            quantity=item.quantity
                        )
                    )
                    total_products += item.quantity
            
            result.append(
                WarehouseInventoryDTO(
                    warehouse_id=warehouse.id,
                    warehouse_name=warehouse.name,
                    warehouse_location=warehouse.location,
                    total_products_count=total_products,
                    items=items_detail
                )
            )
        
        return result
