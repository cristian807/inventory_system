import pytest
from unittest.mock import AsyncMock, MagicMock
from app.domain.entities.entities import User
from app.application.use_cases.user_use_cases import (
    CreateUserUseCase, GetUserByIdUseCase, GetAllUsersUseCase
)
from app.application.dtos.dtos import UserCreateDTO


@pytest.mark.asyncio
async def test_create_user():
    mock_repository = AsyncMock()
    mock_user = User(
        id=1,
        first_name="John",
        last_name="Doe",
        email="john@example.com",
        phone="1234567890",
        gender="male",
        nationality="USA",
        nat="US",
        username="johndoe",
        picture_url="https://example.com/pic.jpg"
    )
    mock_repository.create.return_value = mock_user
    
    use_case = CreateUserUseCase(mock_repository)
    
    user_dto = UserCreateDTO(
        first_name="John",
        last_name="Doe",
        email="john@example.com",
        phone="1234567890",
        gender="male",
        nationality="USA",
        nat="US",
        username="johndoe",
        picture_url="https://example.com/pic.jpg"
    )
    
    result = await use_case.execute(user_dto)
    
    assert result.first_name == "John"
    assert result.last_name == "Doe"
    assert result.email == "john@example.com"


@pytest.mark.asyncio
async def test_get_user_by_id():
    mock_repository = AsyncMock()
    mock_user = User(
        id=1,
        first_name="John",
        last_name="Doe",
        email="john@example.com",
        phone="1234567890",
        gender="male",
        nationality="USA",
        nat="US",
        username="johndoe"
    )
    mock_repository.get_by_id.return_value = mock_user
    
    use_case = GetUserByIdUseCase(mock_repository)
    result = await use_case.execute(1)
    
    assert result.id == 1
    assert result.first_name == "John"


@pytest.mark.asyncio
async def test_get_all_users():
    mock_repository = AsyncMock()
    mock_users = [
        User(id=1, first_name="John", last_name="Doe", email="john@example.com", 
             phone="1234567890", gender="male", nationality="USA", nat="US", username="johndoe"),
        User(id=2, first_name="Jane", last_name="Doe", email="jane@example.com",
             phone="1234567891", gender="female", nationality="USA", nat="US", username="janedoe")
    ]
    mock_repository.get_all.return_value = mock_users
    
    use_case = GetAllUsersUseCase(mock_repository)
    result = await use_case.execute(0, 100)
    
    assert len(result) == 2
    assert result[0].first_name == "John"
    assert result[1].first_name == "Jane"
