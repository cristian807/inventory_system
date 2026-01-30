"""
Dependencias de seguridad para FastAPI
"""
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from app.infrastructure.persistence.database import get_db
from app.infrastructure.persistence.repositories import UserRepository
from app.infrastructure.security.jwt_handler import decode_access_token
from app.infrastructure.persistence.models import UserRole

security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    session: AsyncSession = Depends(get_db)
):
    """
    Obtiene el usuario actual desde el token JWT
    
    Args:
        credentials: Credenciales HTTP Bearer
        session: Sesión de base de datos
    
    Returns:
        Usuario autenticado con bodegas asignadas cargadas
    
    Raises:
        HTTPException: Si el token es inválido o el usuario no existe
    """
    from sqlalchemy import select
    from sqlalchemy.orm import selectinload
    from app.infrastructure.persistence.models import UserModel
    
    token = credentials.credentials
    payload = decode_access_token(token)
    
    user_id: Optional[int] = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Cargar usuario con sus bodegas asignadas
    result = await session.execute(
        select(UserModel)
        .options(selectinload(UserModel.assigned_warehouses))
        .where(UserModel.id == int(user_id))
    )
    user = result.scalar_one_or_none()
    
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no encontrado",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return user


async def require_admin(current_user = Depends(get_current_user)):
    """
    Verifica que el usuario actual sea administrador
    
    Args:
        current_user: Usuario actual obtenido del token
    
    Returns:
        Usuario administrador
    
    Raises:
        HTTPException: Si el usuario no es administrador
    """
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos de administrador para realizar esta acción"
        )
    return current_user


async def get_current_user_optional(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(HTTPBearer(auto_error=False)),
    session: AsyncSession = Depends(get_db)
):
    """
    Obtiene el usuario actual si hay token, sino retorna None
    Útil para endpoints que pueden ser accedidos con o sin autenticación
    """
    if credentials is None:
        return None
    
    try:
        return await get_current_user(credentials, session)
    except HTTPException:
        return None
