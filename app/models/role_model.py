from db import db
from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean
)
class RoleModel(db.Model):
    __tablename__ = 'roles'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    status = Column(Boolean, default=True)