from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.persistence.database import get_db
from app.infrastructure.persistence.repositories import UserRepository
from app.infrastructure.security import hash_password, verify_password, create_access_token
from app.application.dtos.dtos import UserRegisterDTO, UserLoginDTO, TokenDTO, UserResponseDTO
from app.infrastructure.persistence.models import UserModel, UserRole

router = APIRouter(prefix="/api/auth", tags=["authentication"])


@router.post("/register", response_model=TokenDTO, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserRegisterDTO, session: AsyncSession = Depends(get_db)):
    repository = UserRepository(session)
    
    # Verificar si el usuario ya existe
    existing_user = await repository.get_by_username(user_data.username)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El nombre de usuario ya está en uso"
        )
    
    # Verificar si el email ya existe
    existing_email = await repository.get_by_email(user_data.email)
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El email ya está registrado"
        )
    
    hashed_password = hash_password(user_data.password)
    
    user_model = UserModel(
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        email=user_data.email,
        phone=user_data.phone,
        gender=user_data.gender,
        nationality=user_data.nationality,
        nat=user_data.nat,
        username=user_data.username,
        hashed_password=hashed_password,
        role=UserRole.USER, # Rol por defecto de usuario normal
        picture_url=user_data.picture_url
    )
    
    user = await repository.create(user_model)
    
    access_token = create_access_token(
        data={"sub": str(user.id), "username": user.username, "role": user.role.value}
    )
    
    return TokenDTO(
        access_token=access_token,
        user=UserResponseDTO.model_validate(user)
    )


@router.post("/login", response_model=TokenDTO)
async def login(credentials: UserLoginDTO, session: AsyncSession = Depends(get_db)):

    repository = UserRepository(session)
    
    # Buscar usuario por username
    user = await repository.get_by_username(credentials.username)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos"
        )
    
    # Verificar contraseña
    if not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos"
        )
    
    # Crear token
    access_token = create_access_token(
        data={"sub": str(user.id), "username": user.username, "role": user.role.value}
    )
    
    return TokenDTO(
        access_token=access_token,
        user=UserResponseDTO.model_validate(user)
    )


@router.post("/register-admin", response_model=TokenDTO, status_code=status.HTTP_201_CREATED)
async def register_admin(user_data: UserRegisterDTO, session: AsyncSession = Depends(get_db)):
    repository = UserRepository(session)
    
    # Verificar si el usuario ya existe
    existing_user = await repository.get_by_username(user_data.username)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El nombre de usuario ya está en uso"
        )
    
    # Verificar si el email ya existe
    existing_email = await repository.get_by_email(user_data.email)
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El email ya está registrado"
        )
    
    # Crear el nuevo usuario admin
    hashed_password = hash_password(user_data.password)
    
    user_model = UserModel(
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        email=user_data.email,
        phone=user_data.phone,
        gender=user_data.gender,
        nationality=user_data.nationality,
        nat=user_data.nat,
        username=user_data.username,
        hashed_password=hashed_password,
        role=UserRole.ADMIN,  # Rol de administrador
        picture_url=user_data.picture_url
    )
    
    user = await repository.create(user_model)
    
    # Crear token
    access_token = create_access_token(
        data={"sub": str(user.id), "username": user.username, "role": user.role.value}
    )
    
    return TokenDTO(
        access_token=access_token,
        user=UserResponseDTO.model_validate(user)
    )
