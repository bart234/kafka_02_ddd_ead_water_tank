from abc import ABC, abstractmethod
from dataclasses import dataclass
from app.models_data_structures.water_structure import *
from app.models_data_base_structures.db_water_structure import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine,select

class DataABC(ABC):
    @abstractmethod
    def add(self)->dict[WaterTankFeatures]:
        raise NotImplementedError

class SQLAlchemyRepository(DataABC):
    def __init__(self,session):
        self.session = session

    def add(self,data:db_WaterTanks):
        self.session.add(data)
        self.session.commit()

    def select(self,attr_name: str, value_to_search:str)->db_WaterTanks:
        query = select(db_WaterTanks).where(db_WaterTanks.getattr(db_WaterTanks,attr_name)==value_to_search)
        result = self.session.scalar(query)
        return result