from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class User:
    id: Optional[int] = None
    first_name: str = ""
    last_name: str = ""
    email: str = ""
    phone: str = ""
    gender: str = ""
    nationality: str = ""
    nat: str = ""
    username: str = ""
    role: Optional[str] = None
    picture_url: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def __eq__(self, other):
        if not isinstance(other, User):
            return False
        return self.id == other.id and self.email == other.email


@dataclass
class Product:
    id: Optional[int] = None
    name: str = ""
    description: str = ""
    price: float = 0.0
    packaging_unit: Optional[str] = "Unidad"
    units_per_package: int = 1
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


@dataclass
class Warehouse:
    id: Optional[int] = None
    name: str = ""
    location: str = ""
    capacity: int = 0
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

@dataclass
class InventoryItem:
    id: Optional[int] = None
    warehouse_id: int = 0
    product_id: int = 0
    quantity: int = 0
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None