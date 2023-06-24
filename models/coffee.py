import enum
from sqlalchemy import *
from sqlalchemy.orm import *

from .database import Base
from .coffee_type import CoffeeTypeModel
from .bean import BeanModel


class TimeOfDayEnum(enum.Enum):
    MORNING = 'MORNING'
    NOON = 'NOON'
    AFTERNOON = 'AFTERNOON'
    NIGHT = 'NIGHT'


class CoffeeModel(Base):
    __tablename__ = 'coffee'
    id = Column(Integer, primary_key=True)
    sweetener = Column(String)
    time_of_day = Column(Enum(TimeOfDayEnum), nullable=False)
    date = Column(Date, default=func.now())
    coffee_type_id = Column(Integer, ForeignKey('coffee_type.id'), nullable=False)
    bean_id = Column(Integer, ForeignKey('bean.id')) 

    coffee_type = relationship(CoffeeTypeModel, backref=backref('types', uselist=True, cascade='delete,all'))
    bean = relationship(BeanModel, backref=backref('bean', uselist=True, cascade='delete,all'))
