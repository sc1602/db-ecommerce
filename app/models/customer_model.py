from db import db
from sqlalchemy import (
    Column,
    Integer,
    String,
)

class CustomerModel(db.Model):
    __tablename__ = 'customers'
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    last_name = Column(String(100))
    email = Column(String(100))
    address = Column(String(250))
    document_number = Column(String(11), unique=True)

    def __repr__(self):
        return f'<CustomerModel {self.document_number}>'