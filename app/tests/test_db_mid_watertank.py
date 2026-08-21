from app.db_access_layer.db_mid_layer import SQLAlchemyRepository
from app.models_data_base_structures.db_water_structure import db_WaterTanks
from sqlalchemy import select
import pytest


class TestWaterTank:
    def test_add_wt(self,db_test_session):
        self.repo = SQLAlchemyRepository(db_test_session)
        test_tank_id = 'tank_2201'
        wt = db_WaterTanks(tank_tag=test_tank_id,
                        name='my_test_tank',
                        capacity=10,
                        owner='admin',
                        status=0,
                        valve_status=0)
        self.repo.add(wt)

        query = select(db_WaterTanks).where(db_WaterTanks.tank_tag==test_tank_id)
        result =db_test_session.scalar(query)
        assert result==wt

    def test_select_wt_by_attr(self,db_test_session,add_dummy_wt_to_db):
        test_tank_id = 'test_tank_fixtures'
        self.repository = SQLAlchemyRepository(db_test_session)
        result = self.repository.get(test_tank_id)
        tank = db_WaterTanks(tank_tag=test_tank_id,
                        name='my_test_tank',
                        capacity=10,
                        owner='admin',
                        status=0,
                        valve_status=0)
        assert result == tank

    def test_update_and_return_wt(self,db_test_session,add_dummy_wt_to_db):
        test_tank_id = 'test_tank_fixtures_2nd'
        self.repository = SQLAlchemyRepository(db_test_session)
        capacity_before = (self.repository.get(test_tank_id)).capacity
        result = self.repository.update_and_return(test_tank_id,'capacity',900)
        assert result.tank_tag == test_tank_id
        assert result.capacity != capacity_before
        assert result.capacity == 900

    def test_delete(self,db_test_session,add_dummy_wt_to_db):
        test_tank_id = 'test_tank_fixtures_3rd'
        self.repository = SQLAlchemyRepository(db_test_session)
        result = self.repository.delete(test_tank_id)
        assert result == True
        assert self.repository.get(test_tank_id) == None

    def test_get_specific_attr(self,db_test_session,add_dummy_wt_to_db):
        test_tank_id = 'test_tank_fixtures'
        self.repository = SQLAlchemyRepository(db_test_session)
        result =self.repository.get_specific_attr(test_tank_id,'owner')
        assert result == 'admin'
