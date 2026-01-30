from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.entities.entities import User, Product, Warehouse, InventoryItem


class IUserRepository(ABC):
    
    @abstractmethod
    async def create(self, user: User) -> User:
        pass
    
    @abstractmethod
    async def get_by_id(self, user_id: int) -> Optional[User]:
        pass
    
    @abstractmethod
    async def get_all(self, skip: int = 0, limit: int = 100) -> List[User]:
        pass
    
    @abstractmethod
    async def get_by_email(self, email: str) -> Optional[User]:
        pass
    
    @abstractmethod
    async def update(self, user_id: int, user: User) -> User:
        pass
    
    @abstractmethod
    async def delete(self, user_id: int) -> bool:
        pass


class IProductRepository(ABC):
    
    @abstractmethod
    async def create(self, product: Product) -> Product:
        pass
    
    @abstractmethod
    async def get_by_id(self, product_id: int) -> Optional[Product]:
        pass
    
    @abstractmethod
    async def get_all(self, skip: int = 0, limit: int = 100) -> List[Product]:
        pass
    
    @abstractmethod
    async def update(self, product_id: int, product: Product) -> Product:
        pass
    
    @abstractmethod
    async def delete(self, product_id: int) -> bool:
        pass


class IWarehouseRepository(ABC):
    
    @abstractmethod
    async def create(self, warehouse: Warehouse) -> Warehouse:
        pass
    
    @abstractmethod
    async def get_by_id(self, warehouse_id: int) -> Optional[Warehouse]:
        pass
    
    @abstractmethod
    async def get_all(self, skip: int = 0, limit: int = 100) -> List[Warehouse]:
        pass
    
    @abstractmethod
    async def update(self, warehouse_id: int, warehouse: Warehouse) -> Warehouse:
        pass
    
    @abstractmethod
    async def delete(self, warehouse_id: int) -> bool:
        pass

class IInventoryRepository(ABC):

    @abstractmethod
    async def create(self, inventory_item: InventoryItem) -> InventoryItem:
        pass
    
    @abstractmethod
    async def get_by_id(self, inventory_id: int) -> Optional[InventoryItem]:
        pass
    
    @abstractmethod
    async def get_by_warehouse_and_product(self, warehouse_id: int, product_id: int) -> Optional[InventoryItem]:
        pass
    
    @abstractmethod
    async def get_by_warehouse(self, warehouse_id: int, skip: int = 0, limit: int = 100) -> List[InventoryItem]:
        pass
    
    @abstractmethod
    async def get_all(self, skip: int = 0, limit: int = 100) -> List[InventoryItem]:
        pass
    
    @abstractmethod
    async def update(self, inventory_id: int, inventory_item: InventoryItem) -> InventoryItem:
        pass
    
    @abstractmethod
    async def delete(self, inventory_id: int) -> bool:
        pass
    
    # Métodos para conteos de inventario
    @abstractmethod
    async def create_count(self, count):
        pass
    
    @abstractmethod
    async def get_count_by_id(self, count_id: int):
        pass
    
    @abstractmethod
    async def get_counts(self, warehouse_id: Optional[int] = None, status: Optional[str] = None):
        pass
    
    @abstractmethod
    async def update_count(self, count):
        pass