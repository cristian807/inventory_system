from __future__ import annotations
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


class UserRegisterDTO(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    gender: str
    nationality: str
    nat: str
    username: str
    password: str = Field(..., min_length=6, max_length=72)
    picture_url: Optional[str] = None


class UserLoginDTO(BaseModel):
    username: str
    password: str


class UserCreateDTO(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    gender: str
    nationality: str
    nat: str
    username: str
    password: Optional[str] = Field(None, min_length=6, max_length=72)
    role: Optional[str] = "user"
    picture_url: Optional[str] = None


class UserResponseDTO(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    phone: str
    gender: str
    nationality: str
    nat: str
    username: str
    role: str
    picture_url: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class TokenDTO(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponseDTO


class LoadUsersResponseDTO(BaseModel):
    total_loaded: int
    message: str
    success: bool


class ProductCreateDTO(BaseModel):
    name: str
    description: str
    price: float
    packaging_unit: Optional[str] = "Unidad" 
    units_per_package: int = 1  


class ProductResponseDTO(BaseModel):
    id: int
    name: str
    description: str
    price: float
    packaging_unit: Optional[str]
    units_per_package: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True


class WarehouseCreateDTO(BaseModel):
    name: str
    location: str
    capacity: int


class WarehouseResponseDTO(BaseModel):
    id: int
    name: str
    location: str
    capacity: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class InventoryItemCreateDTO(BaseModel):
    count_id: Optional[int] = None  
    warehouse_id: int
    product_id: int
    packages_count: int  
    quantity: Optional[int] = None  


class InventoryItemResponseDTO(BaseModel):
    id: int
    count_id: Optional[int]
    warehouse_id: int
    product_id: int
    packages_count: int
    quantity: int  
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class InventoryDetailDTO(BaseModel):
    id: int
    product_id: int
    product_name: str
    product_price: float
    quantity: int


class WarehouseInventoryDTO(BaseModel):
    warehouse_id: int
    warehouse_name: str
    warehouse_location: str
    total_products_count: int
    items: list[InventoryDetailDTO]


class InventoryCountCreateDTO(BaseModel):
    name: str
    cut_off_date: str  
    warehouse_id: int


class InventoryCountResponseDTO(BaseModel):
    id: int
    name: str
    cut_off_date: str
    warehouse_id: int
    warehouse_name: Optional[str] = None
    status: str
    created_by: int
    creator_username: Optional[str] = None
    created_at: datetime
    closed_at: Optional[datetime] = None
    items_count: int = 0

    class Config:
        from_attributes = True


class InventoryCountDetailDTO(BaseModel):
    id: int
    name: str
    cut_off_date: str
    warehouse_id: int
    warehouse_name: str
    status: str
    created_by: int
    creator_username: str
    created_at: datetime
    closed_at: Optional[datetime]
    items: list[InventoryItemResponseDTO]

    class Config:
        from_attributes = True