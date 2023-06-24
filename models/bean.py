import enum
from sqlalchemy import *

from .database import Base


class RoastEnum(enum.Enum):
    LIGHT = 0
    MEDIUM = 1
    DARK = 2

    def __str__(self):
        return str(self.value)


class BeanModel(Base):
    __tablename__ = 'bean'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    roast = Column(Enum(RoastEnum), nullable=False)
