from fastapi import FastAPI,HTTPException

import uuid
from app.models_data_structures.water_structure import *

app = FastAPI()

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


temp_db = {}
features_for_tanks={}


t1= WaterTank(id='22',name='t1',capacity=10,owner='bob',status=0)
temp_db['22']=t1
features_for_tanks['22']=WaterTankFeatures(tank_id='22')


@app.get("/tank/showallfutures",response_model=list[WaterTankFeatures])
def post_show_all_water_containers_features():
    return features_for_tanks.values()

@app.get("/tank/showalltanks",response_model=list[WaterTank])
def post_show_all_water_containers():
    return temp_db.values()

@app.post("/tank/create",response_model=WaterTank)
def create_tank(watertank_creation:WaterTankCreation):
    new_tank =WaterTank(id=str(uuid.uuid4())[0:2],
                 name=watertank_creation.name,
                 capacity=watertank_creation.capacity,
                 owner=watertank_creation.owner
                 )
    features_for_tanks[new_tank.id]=WaterTankFeatures(tank_id=new_tank.id)
    temp_db[new_tank.id]=new_tank
    return new_tank


@app.post("/tank/{tank_id}/check_status",response_model=WaterTankStatusReturn)
def get_tank_status(tank_id:str):
    if tank_id in temp_db.keys():
        return WaterTankStatusReturn(id=tank_id, status=temp_db[tank_id].status)
    else:
        raise HTTPException(status_code=400, detail=f"Tank: {tank_id} do not exist")

@app.post("/tank/{tank_id}/switchoffswitchon",response_model=WaterTankStatusReturn)
def get_tank_turnOff_turnOn(tank_id:str):
    if str(tank_id) in temp_db.keys():
        if temp_db[tank_id].status == 1:
            temp_db[tank_id].status=0
            print(1)
        elif temp_db[tank_id].status == 0:
            temp_db[tank_id].status=1
        else:
             temp_db[tank_id].status = -1
        return WaterTankStatusReturn(id=tank_id, status=temp_db[tank_id].status)
    else:
        raise HTTPException(status_code=400, detail=f"Tank: {tank_id} do not exist")

@app.post("/tank/{tank_id}/switch/{feature_name}",response_model=WaterTankFeatures)
def get_feature_turnOff_turnOn(tank_id:str,feature_name:str):  
    if str(tank_id) in features_for_tanks.keys(): 
        tank_features =  features_for_tanks[tank_id]
        if hasattr(tank_features,feature_name):
            current_val = getattr(tank_features,feature_name)
            if current_val:
                new_value=False
            else:
                new_value=True

            setattr(features_for_tanks[tank_id],feature_name,new_value)
            return features_for_tanks[tank_id]
        else:     
            raise HTTPException(status_code=400, detail=f"Feature: {feature_name} do not exist")
    else:
        raise HTTPException(status_code=400, detail=f"Tank: {tank_id} do not exist")

@app.post("/tank/{tank_id}/check/{feature_name}",response_model=WaterTankOneFeatureStatus)
def get_feature_value_check(tank_id:str,feature_name:str):  
    if str(tank_id) in features_for_tanks.keys(): 
        tank_features =  features_for_tanks[tank_id]
        if hasattr(tank_features,feature_name):
            return WaterTankOneFeatureStatus(feature_name=feature_name,feature_status=getattr(tank_features,feature_name))
        else:     
            raise HTTPException(status_code=400, detail=f"Feature: {feature_name} do not exist")
    else:
        raise HTTPException(status_code=400, detail=f"Tank: {tank_id} do not exist")
    