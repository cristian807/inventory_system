from typing import List, Optional
from app.domain.entities.entities import Warehouse
from app.domain.repositories.repository_interfaces import IWarehouseRepository
from app.application.dtos.dtos import WarehouseCreateDTO, WarehouseResponseDTO


class CreateWarehouseUseCase:
    """Caso de uso para crear una bodega"""
    
    def __init__(self, warehouse_repository: IWarehouseRepository):
        self.warehouse_repository = warehouse_repository
    
    async def execute(self, warehouse_dto: WarehouseCreateDTO) -> WarehouseResponseDTO:
        warehouse = Warehouse(
            name=warehouse_dto.name,
            location=warehouse_dto.location,
            capacity=warehouse_dto.capacity
        )
        created_warehouse = await self.warehouse_repository.create(warehouse)
        return WarehouseResponseDTO.from_orm(created_warehouse)


class GetWarehouseByIdUseCase:
    """Caso de uso para obtener una bodega por ID"""
    
    def __init__(self, warehouse_repository: IWarehouseRepository):
        self.warehouse_repository = warehouse_repository
    
    async def execute(self, warehouse_id: int) -> Optional[WarehouseResponseDTO]:
        warehouse = await self.warehouse_repository.get_by_id(warehouse_id)
        if warehouse:
            return WarehouseResponseDTO.from_orm(warehouse)
        return None


class GetAllWarehousesUseCase:
    """Caso de uso para obtener todas las bodegas"""
    
    def __init__(self, warehouse_repository: IWarehouseRepository):
        self.warehouse_repository = warehouse_repository
    
    async def execute(self, skip: int = 0, limit: int = 100) -> List[WarehouseResponseDTO]:
        warehouses = await self.warehouse_repository.get_all(skip, limit)
        return [WarehouseResponseDTO.from_orm(warehouse) for warehouse in warehouses]


class UpdateWarehouseUseCase:
    """Caso de uso para actualizar una bodega"""
    
    def __init__(self, warehouse_repository: IWarehouseRepository):
        self.warehouse_repository = warehouse_repository
    
    async def execute(self, warehouse_id: int, warehouse_dto: WarehouseCreateDTO) -> WarehouseResponseDTO:
        warehouse = Warehouse(
            name=warehouse_dto.name,
            location=warehouse_dto.location,
            capacity=warehouse_dto.capacity
        )
        updated_warehouse = await self.warehouse_repository.update(warehouse_id, warehouse)
        return WarehouseResponseDTO.from_orm(updated_warehouse)


class DeleteWarehouseUseCase:
    """Caso de uso para eliminar una bodega"""
    
    def __init__(self, warehouse_repository: IWarehouseRepository):
        self.warehouse_repository = warehouse_repository
    
    async def execute(self, warehouse_id: int) -> bool:
        return await self.warehouse_repository.delete(warehouse_id)
