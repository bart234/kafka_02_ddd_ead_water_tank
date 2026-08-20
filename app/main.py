from fastapi import FastAPI,HTTPException
import uuid
from app.models_data_structures.water_structure import *
from app.models_data_base_structures.db_water_structure import *
from app.mappers.map_water_tanks_structures import Mapper_WaterTanks
from app.db_access_layer.db_mid_layer import SQLAlchemyRepository
from sqlalchemy.orm import sessionmaker
from app.db_cfg import engine




app = FastAPI()
Base.metadata.create_all(bind=engine)
#uvicorn main:app --reload

# orgins = [
#     "http://localhost:3000"
# ]

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=orgins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"]
# )



Session=sessionmaker(bind=engine)
session=Session()
    

temp_db = {}
features_for_tanks={}


@app.get("/tank/showallfutures",response_model=list[WaterTankFeatures])
def post_show_all_water_containers_features():
    return features_for_tanks.values()

@app.get("/tank/showalltanks",response_model=list[WaterTank])
def post_show_all_water_containers():
    return temp_db.values()

@app.post("/tank/create",response_model=WaterTank)
def create_tank(watertank_creation:WaterTankCreation):
    new_tank =WaterTank(tank_tag=str(uuid.uuid4())[0:2] if watertank_creation.tank_tag == None else watertank_creation.tank_tag,
                 name=watertank_creation.name,
                 capacity=watertank_creation.capacity,
                 owner=watertank_creation.owner
                 )
    features_for_tanks[new_tank.tank_tag]=WaterTankFeatures(tank_tag=new_tank.tank_tag)
    db_wt = Mapper_WaterTanks.dta_to_db(new_tank)
    db = SQLAlchemyRepository(session)
    db.add(db_wt)
    temp_db[new_tank.tank_tag]=new_tank
    
    return new_tank

# @app.post("/tank/create2",response_model=WaterTank)
# def create_tank(watertank_creation:WaterTankCreation):
#     new_tank =WaterTank(tank_tag=str(uuid.uuid4())[0:2] if watertank_creation.tank_tag == None else watertank_creation.tank_tag,
#                  name=watertank_creation.name,
#                  capacity=watertank_creation.capacity,
#                  owner=watertank_creation.owner
#                  )
#     features_for_tanks[new_tank.tank_tag]=WaterTankFeatures(tank_tag=new_tank.tank_tag)
#     wt=db_WaterTanks(tank_tag=new_tank.tank_tag,
#                      name=new_tank.name,
#                      capacity=new_tank.capacity,
#                      owner=new_tank.owner,
#                      status=new_tank.status,
#                      valve_status=new_tank.valve_status,)


#     session.add(wt)
#     session.commit()
#     temp_db[new_tank.tank_tag]=new_tank
#     return new_tank

@app.post("/tank/{tank_tag}/check_status",response_model=WaterTankStatusReturn)
def get_tank_status(tank_tag:str):
    if tank_tag in temp_db.keys():
        return WaterTankStatusReturn(tank_tag=tank_tag, status=temp_db[tank_tag].status)
    else:
        raise HTTPException(status_code=400, detail=f"Tank: {tank_tag} do not exist")

@app.post("/tank/{tank_tag}/getallfeatures",response_model=WaterTankFeatures)
def get_tank_all_details(tank_tag:str):
    if tank_tag in features_for_tanks.keys():
        return features_for_tanks[tank_tag]
    else:
        raise HTTPException(status_code=400, detail=f"Tank: {tank_tag} do not exist")

@app.post("/tank/{tank_tag}/switchoffswitchon",response_model=WaterTankStatusReturn)
def get_tank_turnOff_turnOn(tank_tag:str):
    if str(tank_tag) in temp_db.keys():
        if temp_db[tank_tag].status == 1:
            temp_db[tank_tag].status=0
            print(1)
        elif temp_db[tank_tag].status == 0:
            temp_db[tank_tag].status=1
        else:
             temp_db[tank_tag].status = -1
        return WaterTankStatusReturn(tank_tag=tank_tag, status=temp_db[tank_tag].status)
    else:
        raise HTTPException(status_code=400, detail=f"Tank: {tank_tag} do not exist")

@app.post("/tank/{tank_tag}/switch/{feature_name}",response_model=WaterTankFeatures)
def get_feature_turnOff_turnOn(tank_tag:str,feature_name:str):  
    if str(tank_tag) in features_for_tanks.keys(): 
        tank_features =  features_for_tanks[tank_tag]
        if hasattr(tank_features,feature_name):
            current_val = getattr(tank_features,feature_name)
            if current_val:
                new_value=False
            else:
                new_value=True

            setattr(features_for_tanks[tank_tag],feature_name,new_value)
            return features_for_tanks[tank_tag]
        else:     
            raise HTTPException(status_code=400, detail=f"Feature: {feature_name} do not exist")
    else:
        raise HTTPException(status_code=400, detail=f"Tank: {tank_tag} do not exist")

@app.post("/tank/{tank_tag}/check/{feature_name}",response_model=WaterTankOneFeatureStatus)
def get_feature_value_check(tank_tag:str,feature_name:str):  
    if str(tank_tag) in features_for_tanks.keys(): 
        tank_features =  features_for_tanks[tank_tag]
        if hasattr(tank_features,feature_name):
            return WaterTankOneFeatureStatus(feature_name=feature_name,feature_status=getattr(tank_features,feature_name))
        else:     
            raise HTTPException(status_code=400, detail=f"Feature: {feature_name} do not exist")
    else:
        raise HTTPException(status_code=400, detail=f"Tank: {tank_tag} do not exist")
    