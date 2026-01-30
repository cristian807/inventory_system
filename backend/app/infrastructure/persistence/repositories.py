from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.domain.entities.entities import User, Product, Warehouse, InventoryItem
from app.domain.repositories.repository_interfaces import IUserRepository, IProductRepository, IWarehouseRepository, IInventoryRepository
from app.infrastructure.persistence.models import UserModel, ProductModel, WarehouseModel, InventoryItemModel, InventoryCountModel, InventoryCountStatus


class UserRepository(IUserRepository):
    
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def create(self, user_model: UserModel) -> UserModel:
        self.session.add(user_model)
        await self.session.commit()
        await self.session.refresh(user_model)
        return user_model
    
    async def get_by_id(self, user_id: int) -> Optional[UserModel]:
        result = await self.session.execute(select(UserModel).where(UserModel.id == user_id))
        return result.scalar_one_or_none()
    
    async def get_by_username(self, username: str) -> Optional[UserModel]:
        """Obtiene un usuario por username"""
        result = await self.session.execute(select(UserModel).where(UserModel.username == username))
        return result.scalar_one_or_none()
    
    async def get_by_email(self, email: str) -> Optional[UserModel]:
        """Obtiene un usuario por email"""
        result = await self.session.execute(select(UserModel).where(UserModel.email == email))
        return result.scalar_one_or_none()
    
    async def get_all(self, skip: int = 0, limit: int = 100) -> List[UserModel]:
        """Obtiene todos los usuarios con paginación"""
        result = await self.session.execute(select(UserModel).offset(skip).limit(limit))
        return list(result.scalars().all())
    
    async def update(self, user_id: int, user: User) -> UserModel:
        """Actualiza un usuario existente"""
        result = await self.session.execute(select(UserModel).where(UserModel.id == user_id))
        user_model = result.scalar_one_or_none()
        if user_model:
            user_model.first_name = user.first_name
            user_model.last_name = user.last_name
            user_model.email = user.email
            user_model.phone = user.phone
            user_model.gender = user.gender
            user_model.nationality = user.nationality
            user_model.nat = user.nat
            user_model.username = user.username
            user_model.picture_url = user.picture_url
            if user.role:
                from app.infrastructure.persistence.models import UserRole
                user_model.role = UserRole(user.role)
            await self.session.commit()
            await self.session.refresh(user_model)
            return user_model
        return None
    
    async def delete(self, user_id: int) -> bool:
        result = await self.session.execute(select(UserModel).where(UserModel.id == user_id))
        user_model = result.scalar_one_or_none()
        if user_model:
            await self.session.delete(user_model)
            await self.session.commit()
            return True
        return False


class ProductRepository(IProductRepository):
    """Implementación del repositorio de Productos"""
    
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def create(self, product: Product) -> Product:
        product_model = ProductModel(
            name=product.name,
            description=product.description,
            price=product.price,
            packaging_unit=product.packaging_unit,
            units_per_package=product.units_per_package
        )
        self.session.add(product_model)
        await self.session.commit()
        await self.session.refresh(product_model)
        
        return Product(
            id=product_model.id,
            name=product_model.name,
            description=product_model.description,
            price=product_model.price,
            packaging_unit=product_model.packaging_unit,
            units_per_package=product_model.units_per_package,
            created_at=product_model.created_at,
            updated_at=product_model.updated_at
        )
    
    async def get_by_id(self, product_id: int) -> Optional[Product]:
        result = await self.session.execute(select(ProductModel).where(ProductModel.id == product_id))
        product_model = result.scalar_one_or_none()
        if product_model:
            return Product(
                id=product_model.id,
                name=product_model.name,
                description=product_model.description,
                price=product_model.price,
                packaging_unit=product_model.packaging_unit,
                units_per_package=product_model.units_per_package,
                created_at=product_model.created_at,
                updated_at=product_model.updated_at
            )
        return None
    
    async def get_all(self, skip: int = 0, limit: int = 100) -> List[Product]:
        result = await self.session.execute(select(ProductModel).offset(skip).limit(limit))
        product_models = result.scalars().all()
        return [
            Product(
                id=pm.id,
                name=pm.name,
                description=pm.description,
                price=pm.price,
                packaging_unit=pm.packaging_unit,
                units_per_package=pm.units_per_package,
                created_at=pm.created_at,
                updated_at=pm.updated_at
            )
            for pm in product_models
        ]
    
    async def update(self, product_id: int, product: Product) -> Product:
        result = await self.session.execute(select(ProductModel).where(ProductModel.id == product_id))
        product_model = result.scalar_one_or_none()
        if product_model:
            product_model.name = product.name
            product_model.description = product.description
            product_model.price = product.price
            product_model.packaging_unit = product.packaging_unit
            product_model.units_per_package = product.units_per_package
            await self.session.commit()
            await self.session.refresh(product_model)
        
        return Product(
            id=product_model.id,
            name=product_model.name,
            description=product_model.description,
            price=product_model.price,
            packaging_unit=product_model.packaging_unit,
            units_per_package=product_model.units_per_package,
            created_at=product_model.created_at,
            updated_at=product_model.updated_at
        )
    
    async def delete(self, product_id: int) -> bool:
        result = await self.session.execute(select(ProductModel).where(ProductModel.id == product_id))
        product_model = result.scalar_one_or_none()
        if product_model:
            await self.session.delete(product_model)
            await self.session.commit()
            return True
        return False


class WarehouseRepository(IWarehouseRepository):
    """Implementación del repositorio de Bodegas"""
    
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def create(self, warehouse: Warehouse) -> Warehouse:
        warehouse_model = WarehouseModel(
            name=warehouse.name,
            location=warehouse.location,
            capacity=warehouse.capacity
        )
        self.session.add(warehouse_model)
        await self.session.commit()
        await self.session.refresh(warehouse_model)
        
        return Warehouse(
            id=warehouse_model.id,
            name=warehouse_model.name,
            location=warehouse_model.location,
            capacity=warehouse_model.capacity,
            created_at=warehouse_model.created_at,
            updated_at=warehouse_model.updated_at
        )
    
    async def get_by_id(self, warehouse_id: int) -> Optional[Warehouse]:
        result = await self.session.execute(select(WarehouseModel).where(WarehouseModel.id == warehouse_id))
        warehouse_model = result.scalar_one_or_none()
        if warehouse_model:
            return Warehouse(
                id=warehouse_model.id,
                name=warehouse_model.name,
                location=warehouse_model.location,
                capacity=warehouse_model.capacity,
                created_at=warehouse_model.created_at,
                updated_at=warehouse_model.updated_at
            )
        return None
    
    async def get_all(self, skip: int = 0, limit: int = 100) -> List[Warehouse]:
        result = await self.session.execute(select(WarehouseModel).offset(skip).limit(limit))
        warehouse_models = result.scalars().all()
        return [
            Warehouse(
                id=wm.id,
                name=wm.name,
                location=wm.location,
                capacity=wm.capacity,
                created_at=wm.created_at,
                updated_at=wm.updated_at
            )
            for wm in warehouse_models
        ]
    
    async def update(self, warehouse_id: int, warehouse: Warehouse) -> Warehouse:
        result = await self.session.execute(select(WarehouseModel).where(WarehouseModel.id == warehouse_id))
        warehouse_model = result.scalar_one_or_none()
        if warehouse_model:
            warehouse_model.name = warehouse.name
            warehouse_model.location = warehouse.location
            warehouse_model.capacity = warehouse.capacity
            await self.session.commit()
            await self.session.refresh(warehouse_model)
        
        return Warehouse(
            id=warehouse_model.id,
            name=warehouse_model.name,
            location=warehouse_model.location,
            capacity=warehouse_model.capacity,
            created_at=warehouse_model.created_at,
            updated_at=warehouse_model.updated_at
        )
    
    async def delete(self, warehouse_id: int) -> bool:
        result = await self.session.execute(select(WarehouseModel).where(WarehouseModel.id == warehouse_id))
        warehouse_model = result.scalar_one_or_none()
        if warehouse_model:
            await self.session.delete(warehouse_model)
            await self.session.commit()
            return True
        return False

class InventoryRepository(IInventoryRepository):
    """Implementación del repositorio de Inventario"""
    
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def create(self, inventory_item) -> InventoryItemModel:
        """Crear nuevo item de inventario (acepta InventoryItemModel directamente)"""
        self.session.add(inventory_item)
        await self.session.commit()
        await self.session.refresh(inventory_item)
        return inventory_item
    
    async def get_by_warehouse_and_product(self, warehouse_id: int, product_id: int) -> Optional[InventoryItem]:
        result = await self.session.execute(
            select(InventoryItemModel).where(
                (InventoryItemModel.warehouse_id == warehouse_id) &
                (InventoryItemModel.product_id == product_id)
            )
        )
        item_model = result.scalar_one_or_none()
        if item_model:
            return InventoryItem(
                id=item_model.id,
                warehouse_id=item_model.warehouse_id,
                product_id=item_model.product_id,
                quantity=item_model.quantity,
                created_at=item_model.created_at,
                updated_at=item_model.updated_at
            )
        return None
    
    async def get_by_warehouse(self, warehouse_id: int, skip: int = 0, limit: int = 100) -> List[InventoryItem]:
        result = await self.session.execute(
            select(InventoryItemModel)
            .where(InventoryItemModel.warehouse_id == warehouse_id)
            .offset(skip)
            .limit(limit)
        )
        items = result.scalars().all()
        return [
            InventoryItem(
                id=item.id,
                warehouse_id=item.warehouse_id,
                product_id=item.product_id,
                quantity=item.quantity,
                created_at=item.created_at,
                updated_at=item.updated_at
            )
            for item in items
        ]
    
    async def get_all(self, skip: int = 0, limit: int = 100) -> List[InventoryItem]:
        result = await self.session.execute(
            select(InventoryItemModel)
            .offset(skip)
            .limit(limit)
        )
        items = result.scalars().all()
        return [
            InventoryItem(
                id=item.id,
                warehouse_id=item.warehouse_id,
                product_id=item.product_id,
                quantity=item.quantity,
                created_at=item.created_at,
                updated_at=item.updated_at
            )
            for item in items
        ]
    
    async def update(self, inventory_id: int, inventory_item: InventoryItem) -> InventoryItem:
        result = await self.session.execute(
            select(InventoryItemModel).where(InventoryItemModel.id == inventory_id)
        )
        existing_item = result.scalar_one_or_none()
        if existing_item:
            existing_item.quantity = inventory_item.quantity
            self.session.add(existing_item)
            await self.session.commit()
            await self.session.refresh(existing_item)
            
            return InventoryItem(
                id=existing_item.id,
                warehouse_id=existing_item.warehouse_id,
                product_id=existing_item.product_id,
                quantity=existing_item.quantity,
                created_at=existing_item.created_at,
                updated_at=existing_item.updated_at
            )
        raise ValueError(f"Inventory item with id {inventory_id} not found")
    
    async def delete(self, inventory_id: int) -> bool:
        result = await self.session.execute(
            select(InventoryItemModel).where(InventoryItemModel.id == inventory_id)
        )
        item_model = result.scalar_one_or_none()
        if item_model:
            await self.session.delete(item_model)
            await self.session.commit()
            return True
        return False
    
    async def get_by_id(self, inventory_id: int) -> Optional[InventoryItemModel]:
        """Obtiene un item de inventario por ID"""
        result = await self.session.execute(
            select(InventoryItemModel).where(InventoryItemModel.id == inventory_id)
        )
        return result.scalar_one_or_none()
    
    # Métodos para conteos de inventario
    async def create_count(self, count: InventoryCountModel) -> InventoryCountModel:
        """Crea un nuevo conteo de inventario"""
        self.session.add(count)
        await self.session.commit()
        await self.session.refresh(count, ['warehouse', 'creator'])
        return count
    
    async def get_count_by_id(self, count_id: int) -> Optional[InventoryCountModel]:
        """Obtiene un conteo por ID con sus relaciones"""
        result = await self.session.execute(
            select(InventoryCountModel)
            .options(
                selectinload(InventoryCountModel.warehouse),
                selectinload(InventoryCountModel.creator),
                selectinload(InventoryCountModel.items)
            )
            .where(InventoryCountModel.id == count_id)
        )
        return result.scalar_one_or_none()
    
    async def get_counts(self, warehouse_id: Optional[int] = None, status: Optional[str] = None) -> List[InventoryCountModel]:
        query = select(InventoryCountModel).options(
            selectinload(InventoryCountModel.warehouse),
            selectinload(InventoryCountModel.creator),
            selectinload(InventoryCountModel.items)
        )
        
        if warehouse_id:
            query = query.where(InventoryCountModel.warehouse_id == warehouse_id)
        
        if status:
            query = query.where(InventoryCountModel.status == InventoryCountStatus(status))
        
        result = await self.session.execute(query)
        return list(result.scalars().all())
    
    async def update_count(self, count: InventoryCountModel) -> InventoryCountModel:
        """Actualiza un conteo existente"""
        self.session.add(count)
        await self.session.commit()
        await self.session.refresh(count, ['warehouse', 'creator', 'items'])
        return count