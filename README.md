# Sistema de Inventario - Fullstack

Aplicación fullstack para gestión de inventario (usuarios, productos, bodegas y conteos de inventario) implementada con FastAPI, React y PostgreSQL.

## Arquitectura

### Backend
- **Framework**: FastAPI
- **Arquitectura**: Clean Architecture (Domain Driven Design)
- **Base de Datos**: PostgreSQL con SQLAlchemy ORM
- **Testing**: Pytest

### Frontend
- **Framework**: React 18
- **Build Tool**: Vite
- **HTTP Client**: Axios

### Base de Datos
- **Sistema**: PostgreSQL
- **ORM**: SQLAlchemy


## Requisitos Previos

- Tener Docker instalado en nuestra maquina


## Correr la aplicacion
Esta aplicacion web esta dockerizado por lo que solo tenemos que correr el comando:

```
docker compose up --build

```

Una vez la plicacion este corriendo podemos acceder al:

-  **Frontend en:** http://localhost:5173/
-  **A la Documentacion del Backend en:** http://localhost:8000/docs


## Usuario Administrador por Defecto

El sistema crea automáticamente un usuario administrador al inicializar la base de datos por primera vez:

- **Username**: `admin`
- **Password**: `admin123`
- **Rol**: ADMIN

Este usuario se crea automáticamente cuando:
- Se ejecuta `docker compose up` por primera vez
- Se elimina y recrea la base de datos (`docker compose down -v`)

## NOTA:
Los usuarios que se sincronizan desde la API extrena tienen una contraseña por defecto que es: **password123**


## Autor

Cristian Mosquera Mosquera
