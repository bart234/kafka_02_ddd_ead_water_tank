from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

#run from level above app : python -m pytest app/tests/test_api.py

def test_show_all_tanks():
    response =client.get("/tank/showalltanks")
    assert response.status_code ==200
    assert response.json()[0]["id"] ==   "22"
    assert response.json()[0]["name"] ==   't1'
    assert response.json()[0]["capacity"] ==   10
    assert response.json()[0]["owner"] ==   'bob'
    assert response.json()[0]["status"] ==   0

def test_show_all_features():
    response =client.get("/tank/showallfutures")
    assert response.status_code ==200
    assert response.json()[0]["tank_id"] ==   "22"
    assert response.json()[0]["autofill"] ==   False
    assert response.json()[0]["sms_service"] ==   False
    assert response.json()[0]["logger"] ==   False



def test_create_water_tank():
    response = client.post("/tank/create/",
                           headers={},
                           json={
                                "name": "tank_003",
                                "capacity": 230,
                                "owner": "owner"
                                }
                            )
    assert response.status_code == 200
    assert response.json()["name"] ==   'tank_003'
    assert response.json()["capacity"] ==   230
    assert response.json()["owner"] ==   'owner'
    assert response.json()["status"] ==   0
    
def test_check_if_features_for_tank_were_created():
    response = client.post("/tank/create/",
                           headers={},
                           json={
                                "name": "tank_004",
                                "capacity": 230,
                                "owner": "owner"
                                }
                            )
    assert response.status_code == 200
    new_water_id = response.json()['id']

    response_get =client.get("/tank/showallfutures")
    assert response_get.status_code ==200    
    for el in response_get.json():
        result = (el if el['tank_id']==new_water_id else None)

    assert result["tank_id"] ==  new_water_id
    assert result["autofill"] ==   False
    assert result["sms_service"] ==   False
    assert result["logger"] ==   False

def test_check_switchoffswitchon_for_tank():
    response = client.post("/tank/create/",
                            headers={},
                            json={
                                "name": "tank_005",
                                "capacity": 230,
                                "owner": "owner"
                                }
                            )
    assert response.status_code == 200
    new_water_id = response.json()['id']
    response_get =client.post(f"/tank/{new_water_id}/check_status")
    assert response_get.status_code == 200    
    response_get.json()['status'] = 1
    response_get =client.post(f"/tank/{new_water_id}/check_status")
    assert response_get.status_code == 200    
    response_get.json()['status'] = 0

 
def test_check_switchoffswitchon_feature_name():
    response = client.post("/tank/create/",
                            headers={},
                            json={
                                "name": "tank_006",
                                "capacity": 230,
                                "owner": "owner"
                                }
                            )
    assert response.status_code == 200
    new_water_id = response.json()['id']


    response_get =client.get("/tank/showallfutures")
    assert response_get.status_code ==200    
    for el in response_get.json():
        result = (el if el['tank_id']==new_water_id else None)

    
    for k in  result.keys():
        if k != "tank_id":
            switched=None
            switched_again=None
            response_feature =client.post(f"/tank/{new_water_id}/switch/{k}")
            assert response_feature.status_code ==200 
            switched=response_feature.json()[k] 
            response_feature_again =client.post(f"/tank/{new_water_id}/switch/{k}")
            assert response_feature_again.status_code ==200 
            switched_again=response_feature_again.json()[k] 
            assert switched!=switched_again

def test_check_check_feature_name():
    response = client.post("/tank/create/",
                            headers={},
                            json={
                                "name": "tank_006",
                                "capacity": 230,
                                "owner": "owner"
                                }
                            )
    assert response.status_code == 200
    new_water_id = response.json()['id']


    response_get =client.get("/tank/showallfutures")
    assert response_get.status_code ==200    
    for el in response_get.json():
        result = (el if el['tank_id']==new_water_id else None)

    for k in  result.keys():
        if k != "tank_id":
            response_feature =client.post(f"/tank/{new_water_id}/check/{k}")
            assert response_feature.status_code ==200 
            assert response_feature.json()['feature_name'] == k
            assert response_feature.json()['feature_status'] == False
