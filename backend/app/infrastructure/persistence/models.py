from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum, Table, Date
from sqlalchemy.orm import relationship
from datetime import datetime
from app.infrastructure.persistence.database import Base
import enum


class UserRole(str, enum.Enum):
    ADMIN = "admin"
    USER = "user"


class InventoryCountStatus(str, enum.Enum):
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CLOSED = "closed"


user_warehouses = Table(
    'user_warehouses',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('warehouse_id', Integer, ForeignKey('warehouses.id'), primary_key=True)
)


class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    phone = Column(String(20), nullable=False)
    gender = Column(String(10), nullable=False)
    nationality = Column(String(100), nullable=False)
    nat = Column(String(10), nullable=False)
    username = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(Enum(UserRole), default=UserRole.USER, nullable=False)
    picture_url = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    assigned_warehouses = relationship("WarehouseModel", secondary=user_warehouses, backref="assigned_users")


class WarehouseModel(Base):
    __tablename__ = "warehouses"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    location = Column(String(200), nullable=False)
    capacity = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class ProductModel(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(String(500), nullable=True)
    price = Column(Float, nullable=False)
    packaging_unit = Column(String(50), nullable=True, default="Unidad")  
    units_per_package = Column(Integer, nullable=False, default=1)  
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class InventoryCountModel(Base):
    __tablename__ = "inventory_counts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)  
    cut_off_date = Column(Date, nullable=False)  
    warehouse_id = Column(Integer, ForeignKey("warehouses.id"), nullable=False)
    status = Column(Enum(InventoryCountStatus), default=InventoryCountStatus.IN_PROGRESS, nullable=False)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    closed_at = Column(DateTime, nullable=True)
    
    warehouse = relationship("WarehouseModel")
    creator = relationship("UserModel")
    items = relationship("InventoryItemModel", back_populates="count")


class InventoryItemModel(Base):
    __tablename__ = "inventory_items"

    id = Column(Integer, primary_key=True, index=True)
    count_id = Column(Integer, ForeignKey("inventory_counts.id"), nullable=True)  
    warehouse_id = Column(Integer, ForeignKey("warehouses.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    packages_count = Column(Integer, nullable=False, default=0)  
    quantity = Column(Integer, nullable=False, default=0)  
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    count = relationship("InventoryCountModel", back_populates="items")
    warehouse = relationship("WarehouseModel")
    product = relationship("ProductModel")