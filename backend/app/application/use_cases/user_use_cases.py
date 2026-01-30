from typing import List, Optional
from app.domain.entities.entities import User
from app.domain.repositories.repository_interfaces import IUserRepository
from app.application.dtos.dtos import UserCreateDTO, UserResponseDTO, LoadUsersResponseDTO
from app.infrastructure.persistence.models import UserModel, UserRole
from app.infrastructure.security.password import hash_password
import httpx


class CreateUserUseCase:
    """Caso de uso para crear un usuario"""
    
    def __init__(self, user_repository: IUserRepository):
        self.user_repository = user_repository
    
    async def execute(self, user_dto: UserCreateDTO) -> UserResponseDTO:
        # Hashear el password si se proporciona
        hashed_password = ""
        if user_dto.password:
            hashed_password = hash_password(user_dto.password)
        
        # Crear UserModel con rol USER por defecto
        user_model = UserModel(
            first_name=user_dto.first_name,
            last_name=user_dto.last_name,
            email=user_dto.email,
            phone=user_dto.phone,
            gender=user_dto.gender,
            nationality=user_dto.nationality,
            nat=user_dto.nat,
            username=user_dto.username,
            hashed_password=hashed_password,
            role=UserRole.USER,  # Rol por defecto USER
            picture_url=user_dto.picture_url
        )
        created_user = await self.user_repository.create(user_model)
        return UserResponseDTO.from_orm(created_user)


class GetUserByIdUseCase:
    """Caso de uso para obtener un usuario por ID"""
    
    def __init__(self, user_repository: IUserRepository):
        self.user_repository = user_repository
    
    async def execute(self, user_id: int) -> Optional[UserResponseDTO]:
        user = await self.user_repository.get_by_id(user_id)
        if user:
            return UserResponseDTO.from_orm(user)
        return None


class GetAllUsersUseCase:
    """Caso de uso para obtener todos los usuarios"""
    
    def __init__(self, user_repository: IUserRepository):
        self.user_repository = user_repository
    
    async def execute(self, skip: int = 0, limit: int = 100) -> List[UserResponseDTO]:
        users = await self.user_repository.get_all(skip, limit)
        return [UserResponseDTO.from_orm(user) for user in users]


class UpdateUserUseCase:
    """Caso de uso para actualizar un usuario"""
    
    def __init__(self, user_repository: IUserRepository):
        self.user_repository = user_repository
    
    async def execute(self, user_id: int, user_dto: UserCreateDTO) -> UserResponseDTO:
        user = User(
            first_name=user_dto.first_name,
            last_name=user_dto.last_name,
            email=user_dto.email,
            phone=user_dto.phone,
            gender=user_dto.gender,
            nationality=user_dto.nationality,
            nat=user_dto.nat,
            username=user_dto.username,
            role=user_dto.role,
            picture_url=user_dto.picture_url
        )
        updated_user = await self.user_repository.update(user_id, user)
        return UserResponseDTO.from_orm(updated_user)


class DeleteUserUseCase:
    """Caso de uso para eliminar un usuario"""
    
    def __init__(self, user_repository: IUserRepository):
        self.user_repository = user_repository
    
    async def execute(self, user_id: int) -> bool:
        return await self.user_repository.delete(user_id)


class LoadUsersUseCase:
    def __init__(self, user_repository: IUserRepository):
        self.user_repository = user_repository
    
    async def execute(self) -> LoadUsersResponseDTO:
        try:
            from app.infrastructure.security import hash_password
            from app.infrastructure.persistence.models import UserModel, UserRole
            
            users_data = await self._fetch_users_from_api()
            
            total_saved = 0
            for user_data in users_data:
                try:
                    # Crear UserModel con password y role
                    user_model = UserModel(
                        first_name=user_data.first_name,
                        last_name=user_data.last_name,
                        email=user_data.email,
                        phone=user_data.phone,
                        gender=user_data.gender,
                        nationality=user_data.nationality,
                        nat=user_data.nat,
                        username=user_data.username,
                        picture_url=user_data.picture_url,
                        hashed_password=hash_password("password123"),  # Password por defecto
                        role=UserRole.USER  # Rol de usuario normal
                    )
                    await self.user_repository.create(user_model)
                    total_saved += 1
                except Exception:
                    continue
            
            return LoadUsersResponseDTO(
                total_loaded=total_saved,
                message=f"Se cargaron {total_saved} usuarios exitosamente. Password por defecto: 'password123'",
                success=True
            )
        except Exception as e:
            return LoadUsersResponseDTO(
                total_loaded=0,
                message=f"Error al cargar usuarios: {str(e)}",
                success=False
            )
    
    async def _fetch_users_from_api(self) -> List[User]:
        url = "https://randomuser.me/api/?results=100"
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(url)
            response.raise_for_status()
            data = response.json()
            
            users = []
            for result in data.get("results", []):
                user = User(
                    first_name=result["name"]["first"],
                    last_name=result["name"]["last"],
                    email=result["email"],
                    phone=result["phone"],
                    gender=result["gender"],
                    nationality=result["location"]["country"],
                    nat=result["nat"],
                    username=result["login"]["username"],
                    picture_url=result["picture"]["large"]
                )
                users.append(user)
            
            return users
