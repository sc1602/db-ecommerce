from db import db
from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    func
)

class UpdateProductLogsModel(db.Model):
    __tablename__ = 'update_product_logs'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    product_id = Column(Integer, ForeignKey('products.id'))
    field = Column(String(20))
    value = Column(String(200))
    created_at = Column(DateTime, default=func.now())