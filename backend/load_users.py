import asyncio
import httpx
import sys
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.persistence.database import AsyncSessionLocal, init_db
from app.domain.entities.entities import User
from app.infrastructure.persistence.repositories import UserRepository


async def fetch_users_from_api():
    url = "https://randomuser.me/api/?results=100"
    
    try:
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
    except httpx.RequestError as e:
        print(f"Error al conectar con la API: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error al procesar la respuesta: {e}")
        sys.exit(1)


async def save_users_to_db(users: list):
    async with AsyncSessionLocal() as session:
        repository = UserRepository(session)
        
        for i, user in enumerate(users, 1):
            try:
                created_user = await repository.create(user)
                print(f"[{i}/100] Usuario {created_user.username} guardado correctamente (ID: {created_user.id})")
            except Exception as e:
                print(f"Error al guardar usuario {user.username}: {e}")
                continue


async def main():
    print("Inicializando la base de datos")
    await init_db()
    print("Base de datos inicializada.")
    
    print("\nObteniendo 100 usuarios de randomuser.me...")
    users = await fetch_users_from_api()
    print(f"Se obtuvieron {len(users)} usuarios exitosamente.")
    
    print("\nGuardando usuarios en la base de datos...")
    await save_users_to_db(users)
    
    print("\n✓ Proceso completado. 100 usuarios cargados en la base de datos.")


if __name__ == "__main__":
    asyncio.run(main())
