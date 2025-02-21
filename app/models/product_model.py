from db import db
from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    Boolean,
    DateTime,
    func,
    ForeignKey
)

class ProductModel(db.Model):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    code = Column(String(7)) # P-12345
    description = Column(String(200))
    image = Column(String(200))
    brand = Column(String(100))
    size = Column(String(50))
    price = Column(Float)
    stock = Column(Integer)
    status = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    category_id = Column(Integer, ForeignKey('categories.id'))