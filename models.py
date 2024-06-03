from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

Base = declarative_base()


class Product(Base):
    __tablename__ = 'productinventory'
    id = Column(Integer, primary_key=True, index=True)
    product = Column(String)
    category = Column(String)
    price = Column(Float)
