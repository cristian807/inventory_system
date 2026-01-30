from typing import List, Optional
from app.domain.entities.entities import Product
from app.domain.repositories.repository_interfaces import IProductRepository
from app.application.dtos.dtos import ProductCreateDTO, ProductResponseDTO


class CreateProductUseCase:
    """Caso de uso para crear un producto"""
    
    def __init__(self, product_repository: IProductRepository):
        self.product_repository = product_repository
    
    async def execute(self, product_dto: ProductCreateDTO) -> ProductResponseDTO:
        product = Product(
            name=product_dto.name,
            description=product_dto.description,
            price=product_dto.price,
            packaging_unit=product_dto.packaging_unit,
            units_per_package=product_dto.units_per_package
        )
        created_product = await self.product_repository.create(product)
        return ProductResponseDTO.from_orm(created_product)


class GetProductByIdUseCase:
    """Caso de uso para obtener un producto por ID"""
    
    def __init__(self, product_repository: IProductRepository):
        self.product_repository = product_repository
    
    async def execute(self, product_id: int) -> Optional[ProductResponseDTO]:
        product = await self.product_repository.get_by_id(product_id)
        if product:
            return ProductResponseDTO.from_orm(product)
        return None


class GetAllProductsUseCase:
    """Caso de uso para obtener todos los productos"""
    
    def __init__(self, product_repository: IProductRepository):
        self.product_repository = product_repository
    
    async def execute(self, skip: int = 0, limit: int = 100) -> List[ProductResponseDTO]:
        products = await self.product_repository.get_all(skip, limit)
        return [ProductResponseDTO.from_orm(product) for product in products]


class UpdateProductUseCase:
    """Caso de uso para actualizar un producto"""
    
    def __init__(self, product_repository: IProductRepository):
        self.product_repository = product_repository
    
    async def execute(self, product_id: int, product_dto: ProductCreateDTO) -> ProductResponseDTO:
        product = Product(
            name=product_dto.name,
            description=product_dto.description,
            price=product_dto.price,
            packaging_unit=product_dto.packaging_unit,
            units_per_package=product_dto.units_per_package
        )
        updated_product = await self.product_repository.update(product_id, product)
        return ProductResponseDTO.from_orm(updated_product)


class DeleteProductUseCase:
    """Caso de uso para eliminar un producto"""
    
    def __init__(self, product_repository: IProductRepository):
        self.product_repository = product_repository
    
    async def execute(self, product_id: int) -> bool:
        return await self.product_repository.delete(product_id)
