from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.persistence.database import get_db
from app.infrastructure.persistence.repositories import UserRepository
from app.application.use_cases.user_use_cases import (
    CreateUserUseCase, GetUserByIdUseCase, GetAllUsersUseCase,
    UpdateUserUseCase, DeleteUserUseCase, LoadUsersUseCase
)
from app.application.dtos.dtos import UserCreateDTO, UserResponseDTO, LoadUsersResponseDTO
from app.infrastructure.security import get_current_user, require_admin
from typing import List

router = APIRouter(prefix="/api/users", tags=["users"])


@router.post("/", response_model=UserResponseDTO)
async def create_user(
    user_dto: UserCreateDTO, 
    session: AsyncSession = Depends(get_db),
    current_user = Depends(require_admin)
):
    repository = UserRepository(session)
    use_case = CreateUserUseCase(repository)
    return await use_case.execute(user_dto)


@router.get("/", response_model=List[UserResponseDTO])
async def get_all_users(
    skip: int = 0, 
    limit: int = 100, 
    session: AsyncSession = Depends(get_db),
    current_user = Depends(require_admin)
):
    repository = UserRepository(session)
    use_case = GetAllUsersUseCase(repository)
    return await use_case.execute(skip, limit)


@router.get("/me", response_model=UserResponseDTO)
async def get_current_user_info(current_user = Depends(get_current_user)):
    return current_user


@router.get("/me/warehouses")
async def get_my_warehouses(
    session: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    from sqlalchemy import select
    from sqlalchemy.orm import selectinload
    from app.infrastructure.persistence.models import UserModel
    
    result = await session.execute(
        select(UserModel)
        .options(selectinload(UserModel.assigned_warehouses))
        .where(UserModel.id == current_user.id)
    )
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    return {
        "user_id": user.id,
        "username": user.username,
        "role": user.role,
        "assigned_warehouses": [{"id": w.id, "name": w.name, "location": w.location} for w in user.assigned_warehouses]
    }


@router.get("/{user_id}", response_model=UserResponseDTO)
async def get_user(
    user_id: int, 
    session: AsyncSession = Depends(get_db),
    current_user = Depends(require_admin)
):
    repository = UserRepository(session)
    use_case = GetUserByIdUseCase(repository)
    user = await use_case.execute(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user


@router.put("/{user_id}", response_model=UserResponseDTO)
async def update_user(
    user_id: int, 
    user_dto: UserCreateDTO, 
    session: AsyncSession = Depends(get_db),
    current_user = Depends(require_admin)
):
    repository = UserRepository(session)
    use_case = UpdateUserUseCase(repository)
    return await use_case.execute(user_id, user_dto)


@router.delete("/{user_id}")
async def delete_user(
    user_id: int, 
    session: AsyncSession = Depends(get_db),
    current_user = Depends(require_admin)
):
    repository = UserRepository(session)
    use_case = DeleteUserUseCase(repository)
    success = await use_case.execute(user_id)
    if not success:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return {"message": "Usuario eliminado correctamente"}


@router.post("/load", response_model=LoadUsersResponseDTO)
async def load_users(
    session: AsyncSession = Depends(get_db),
    current_user = Depends(require_admin)
):
    repository = UserRepository(session)
    use_case = LoadUsersUseCase(repository)
    return await use_case.execute()


@router.post("/{user_id}/assign-warehouses")
async def assign_warehouses_to_user(
    user_id: int,
    warehouse_ids: List[int],
    session: AsyncSession = Depends(get_db),
    current_user = Depends(require_admin)
):
    from sqlalchemy import select
    from sqlalchemy.orm import selectinload
    from app.infrastructure.persistence.models import UserModel, WarehouseModel
    
    result = await session.execute(
        select(UserModel)
        .options(selectinload(UserModel.assigned_warehouses))
        .where(UserModel.id == user_id)
    )
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    result = await session.execute(select(WarehouseModel).where(WarehouseModel.id.in_(warehouse_ids)))
    warehouses = list(result.scalars().all())
    
    if len(warehouses) != len(warehouse_ids):
        raise HTTPException(status_code=404, detail="Una o más bodegas no encontradas")
    
    user.assigned_warehouses = warehouses
    await session.commit()
    await session.refresh(user)
    
    return {
        "message": f"Bodegas asignadas exitosamente al usuario {user.username}",
        "user_id": user_id,
        "assigned_warehouses": [{"id": w.id, "name": w.name} for w in warehouses]
    }


@router.get("/{user_id}/warehouses")
async def get_user_warehouses(
    user_id: int,
    session: AsyncSession = Depends(get_db),
    current_user = Depends(require_admin)
):
    from sqlalchemy import select
    from sqlalchemy.orm import selectinload
    from app.infrastructure.persistence.models import UserModel
    
    result = await session.execute(
        select(UserModel)
        .options(selectinload(UserModel.assigned_warehouses))
        .where(UserModel.id == user_id)
    )
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    return {
        "user_id": user_id,
        "username": user.username,
        "role": user.role,
        "assigned_warehouses": [{"id": w.id, "name": w.name, "location": w.location} for w in user.assigned_warehouses]
    }
