from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.presentation.api.routes import users, products, warehouses, inventory, auth, inventory_counts
from app.infrastructure.persistence.database import init_db

app = FastAPI(
    title="System Inventory API",
    description="API para gestión de inventario con usuarios, productos y bodegas",
    version="1.0.0",
    redirect_slashes=True  # Evitar redirecciones que pierden headers de autenticación
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rutas de autenticación (públicas)
app.include_router(auth.router)

# Rutas de recursos
app.include_router(users.router)
app.include_router(products.router)
app.include_router(warehouses.router)
app.include_router(inventory.router)
app.include_router(inventory_counts.router)


@app.on_event("startup")
async def startup():
    await init_db()


@app.get("/health", tags=["health"])
async def health_check():
    return {"status": "ok", "message": "API funcionando correctamente"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
