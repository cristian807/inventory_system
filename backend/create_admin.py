import asyncio
from app.infrastructure.persistence.database import get_db
from app.infrastructure.persistence.models import UserModel, UserRole
from app.infrastructure.security.password import hash_password

async def create_admin():
    async for session in get_db():
        # Verificar si ya existe
        from sqlalchemy import select
        result = await session.execute(select(UserModel).where(UserModel.username == 'admin'))
        existing = result.scalar_one_or_none()
        
        if existing:
            print("Usuario admin ya existe")
            return
        
        user = UserModel(
            first_name='Admin',
            last_name='System',
            username='admin',
            email='admin@example.com',
            phone='0000000000',
            gender='male',
            nationality='Colombian',
            nat='CO',
            hashed_password=hash_password('admin123'),
            role=UserRole.ADMIN
        )
        session.add(user)
        await session.commit()
        print("✓ Usuario admin creado exitosamente")

if __name__ == "__main__":
    asyncio.run(create_admin())
