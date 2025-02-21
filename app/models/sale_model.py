from db import db
from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    DateTime,
    ForeignKey,
    func,
    Enum as SQLAlchemyEnum
)
from sqlalchemy.orm import relationship
from enum import Enum
from app.models.sale_detail_model import SaleDetailModel
from app.models.customer_model import CustomerModel

class SaleStatus(Enum):
    PENDING = 'PENDING'
    COMPLETED = 'COMPLETED'
    CANCELLED = 'CANCELLED'

class SaleModel(db.Model):
    __tablename__ = 'sales'
    id = Column(Integer, primary_key=True)
    code = Column(String(8), unique=True)
    total = Column(Float)
    status = Column(SQLAlchemyEnum(SaleStatus), default=SaleStatus.PENDING)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    customer_id = Column(Integer, ForeignKey('customers.id'))

    sale_details = relationship(SaleDetailModel)
    customer = relationship(CustomerModel)

    def __repr__(self):
        return f'<SaleModel {self.code}>'