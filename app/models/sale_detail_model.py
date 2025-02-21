from db import db
from sqlalchemy import (
    Column,
    Integer,
    Float,
    ForeignKey
)
from sqlalchemy.orm import relationship
from app.models.product_model import ProductModel

class SaleDetailModel(db.Model):
    __tablename__ = 'sale_details'
    id = Column(Integer, primary_key=True)
    quantity = Column(Integer)
    price = Column(Float)
    subtotal = Column(Float)
    product_id = Column(Integer, ForeignKey('products.id'))
    sale_id = Column(Integer, ForeignKey('sales.id'))

    product = relationship(ProductModel)