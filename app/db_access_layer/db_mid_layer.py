from abc import ABC, abstractmethod
from dataclasses import dataclass
from app.models_data_structures.water_structure import *
from app.models_data_base_structures.db_water_structure import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine,select,update,delete

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

    def get(self,tank_tag:str)->db_WaterTanks:
        query = select(db_WaterTanks).where(db_WaterTanks.tank_tag==tank_tag)
        result = self.session.scalar(query)
        return result    

    def get_specific_attr(self,tank_tag:str,attr_name: str):
        return getattr(self.get(tank_tag),attr_name)    

    #TODO: to remove - not in use in prod
    def select_all(self)->list[db_WaterTanks]:
        query = select(db_WaterTanks)
        result = self.session.scalars(query)
        return result

    def update(self,tank_tag:str,attr_to_change: str,new_value)->bool:        
        upd_query = update(db_WaterTanks).\
                    where(db_WaterTanks.tank_tag==tank_tag).\
                    values({getattr(db_WaterTanks,attr_to_change):new_value})
        result = self.session.execute(upd_query)
        self.session.commit()
        return result.rowcount >0

    def update_and_return(self,tank_tag:str,attr_to_change: str,new_value)->db_WaterTanks:
        if self.update(tank_tag,attr_to_change,new_value) >0:
            return self.get(tank_tag)
        else:
            None

    def delete(self,tank_tag:str)->bool:        
        del_query = delete(db_WaterTanks).\
                    where(db_WaterTanks.tank_tag==tank_tag)
        result = self.session.execute(del_query)
        self.session.commit()
        return result.rowcount > 0