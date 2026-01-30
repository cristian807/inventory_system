import pytest
from unittest.mock import AsyncMock
from app.domain.entities.entities import Product
from app.application.use_cases.product_use_cases import (
    CreateProductUseCase, GetProductByIdUseCase, GetAllProductsUseCase
)
from app.application.dtos.dtos import ProductCreateDTO


@pytest.mark.asyncio
async def test_create_product():
    mock_repository = AsyncMock()
    mock_product = Product(
        id=1,
        name="Laptop",
        description="High performance laptop",
        price=999.99,
        warehouse_id=1
    )
    mock_repository.create.return_value = mock_product
    
    use_case = CreateProductUseCase(mock_repository)
    
    product_dto = ProductCreateDTO(
        name="Laptop",
        description="High performance laptop",
        price=999.99,
        warehouse_id=1
    )
    
    result = await use_case.execute(product_dto)
    
    assert result.name == "Laptop"
    assert result.price == 999.99


@pytest.mark.asyncio
async def test_get_product_by_id():
    mock_repository = AsyncMock()
    mock_product = Product(
        id=1,
        name="Laptop",
        description="High performance laptop",
        price=999.99,
        warehouse_id=1
    )
    mock_repository.get_by_id.return_value = mock_product
    
    use_case = GetProductByIdUseCase(mock_repository)
    result = await use_case.execute(1)
    
    assert result.id == 1
    assert result.name == "Laptop"


@pytest.mark.asyncio
async def test_get_all_products():
    mock_repository = AsyncMock()
    mock_products = [
        Product(id=1, name="Laptop", description="High performance laptop", price=999.99, warehouse_id=1),
        Product(id=2, name="Mouse", description="Wireless mouse", price=29.99, warehouse_id=1)
    ]
    mock_repository.get_all.return_value = mock_products
    
    use_case = GetAllProductsUseCase(mock_repository)
    result = await use_case.execute(0, 100)
    
    assert len(result) == 2
    assert result[0].name == "Laptop"
    assert result[1].name == "Mouse"
