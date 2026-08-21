
from app.main import app
from app.models_data_structures.water_structure import WaterTankFeatures

# client = TestClient(app)
#run from level above app : python -m pytest app/tests/test_api.py
#API tests - just paths, send request check http.status and answer resturn structure

def test_show_all_tanks(client,test_data_for_api_check):
    response =client.get("/tank/showalltanks")
    assert response.status_code ==200
    assert response.json()[0]["tank_tag"] ==  test_data_for_api_check['tank_tag']
    assert response.json()[0]["name"] ==  test_data_for_api_check['name']
    assert response.json()[0]["capacity"] ==  test_data_for_api_check['capacity']
    assert response.json()[0]["owner"] ==  test_data_for_api_check['owner']
    assert response.json()[0]["status"] ==   test_data_for_api_check['status']

def test_show_all_features(client,test_data_for_api_check):
    response =client.get("/tank/showallfutures")
    assert response.status_code ==200
    assert response.json()[0]["tank_tag"] ==   test_data_for_api_check['tank_tag']
    assert response.json()[0]["autofill"] ==   False
    assert response.json()[0]["sms_service"] ==   False
    assert response.json()[0]["logger"] ==   False

def test_create_water_tank(client):
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
    assert response.json()["status"] ==  0
   
def test_check_if_features_for_tank_were_created(client):
    response = client.post("/tank/create/",
                           headers={},
                           json={
                                "tank_tag":"tank_004",
                                "name": "name_004",
                                "capacity": 230,
                                "owner": "owner"
                                }
                            )
    assert response.status_code == 200
    result =client.post(f"/tank/{"tank_004"}/getallfeatures")
    assert result.status_code ==200    
    result_data=result.json()
    assert result_data["tank_tag"] ==  "tank_004"
    assert result_data["autofill"] ==   False
    assert result_data["sms_service"] ==   False
    assert result_data["logger"] ==   False

def test_check_switchoffswitchon_for_tank(client):
    response = client.post("/tank/create/",
                            headers={},
                            json={
                                "tank_tag": "tank_005",
                                "name": "name_005",
                                "capacity": 230,
                                "owner": "owner"
                                }
                            )
    assert response.status_code == 200
    new_water_id = response.json()['tank_tag']
    response_get =client.post(f"/tank/{new_water_id}/check_status")
    assert response_get.status_code == 200    
    response_get.json()['status'] = 1
    response_get =client.post(f"/tank/{new_water_id}/check_status")
    assert response_get.status_code == 200    
    response_get.json()['status'] = 0
 
def test_check_switchoffswitchon_feature_name(client,test_data_for_api_check):
    test_tank_tag = test_data_for_api_check['tank_tag']
    for k in  list(WaterTankFeatures.model_fields.keys())[1:]:
        switched=None
        switched_again=None
        response_feature =client.post(f"/tank/{test_tank_tag}/switch/{k}")
        assert response_feature.status_code ==200 
        switched=response_feature.json()[k] 
        response_feature_again =client.post(f"/tank/{test_tank_tag}/switch/{k}")
        assert response_feature_again.status_code ==200 
        switched_again=response_feature_again.json()[k] 
        assert switched!=switched_again

def test_check_check_feature_name(client,test_data_for_api_check):
    test_tank_tag = test_data_for_api_check['tank_tag']
    response_get =client.post(f"/tank/{test_tank_tag}/getallfeatures")
    assert response_get.status_code ==200    
    for k in  list(WaterTankFeatures.model_fields.keys())[1:]:
        response_feature =client.post(f"/tank/{test_tank_tag}/check/{k}")
        assert response_feature.status_code ==200 
        assert response_feature.json()['feature_name'] == k
        assert response_feature.json()['feature_status'] == False
