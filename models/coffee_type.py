from sqlalchemy import *

from .database import Base

class CoffeeTypeModel(Base):
    __tablename__ = 'coffee_type'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
