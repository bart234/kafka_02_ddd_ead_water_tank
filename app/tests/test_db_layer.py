
from app.db_access_layer.db_mid_layer import SQLAlchemyRepository
from app.models_data_base_structures.db_water_structure import db_WaterTanks
from sqlalchemy import select

def test_add_wt(db_test_session):
    repo = SQLAlchemyRepository(db_test_session)
    test_tank_id = 'tank_2201'
    wt = db_WaterTanks(tank_tag=test_tank_id,
                     name='my_test_tank',
                     capacity=10,
                     owner='admin',
                     status=0,
                     valve_status=0)
    repo.add(wt)

    query = select(db_WaterTanks).where(db_WaterTanks.tank_tag==test_tank_id)
    result =db_test_session.scalar(query)
    assert result==wt

# def test_create_item():
#     pass

# def test_get_item_by_id():
#     pass

# def test_create_wt():
#     pass

# def test_get_wt_by_id():
#     pass

# def test_get_all_wt():
#     pass

# def test_edit_wt():
#     pass

# def test_delete_wt():
#     pass