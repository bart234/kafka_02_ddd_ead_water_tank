from pydantic import BaseModel


class WaterTankCreation(BaseModel):
    name:str
    capacity:int
    owner:str

class WaterTankFeatures(BaseModel):
    tank_id:str
    autofill:bool =False
    sms_service: bool =False
    logger:bool =False

class WaterTankOneFeatureStatus(BaseModel):
    feature_name: str
    feature_status: bool    


class WaterTank(WaterTankCreation):
    id:str
    status:int =0
    valve_status:int = 0

class WaterTankStatusReturn(BaseModel):
    id:str
    status:int

class WaterTankWaterLevelReturn(BaseModel):
    id:str
    water_level:int
