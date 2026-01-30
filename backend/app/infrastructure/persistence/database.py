from sqlalchemy import create_engine, select
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.pool import NullPool
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:password@localhost:5432/system_inventory")

ASYNC_DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")

engine = create_async_engine(
    ASYNC_DATABASE_URL,
    echo=True,
    future=True,
    pool_pre_ping=True,
    poolclass=NullPool
)

AsyncSessionLocal = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False, future=True
)

Base = declarative_base()


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session


async def create_default_admin():
    from app.infrastructure.persistence.models import UserModel, UserRole
    from app.infrastructure.security import hash_password
    
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(UserModel).where(UserModel.username == "admin")
        )
        existing_admin = result.scalar_one_or_none()
        
        if not existing_admin:
            admin_user = UserModel(
                first_name="Admin",
                last_name="System",
                email="admin@system.com",
                phone="0000000000",
                gender="male",
                nationality="System",
                nat="SY",
                username="admin",
                hashed_password=hash_password("admin123"),
                role=UserRole.ADMIN,
                picture_url=None
            )
            session.add(admin_user)
            await session.commit()
            print("✅ Usuario admin creado por defecto")
            print("   Username: admin")
            print("   Password: admin123")
        else:
            print("ℹ️  Usuario admin ya existe")


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    await create_default_admin()
