from fastapi.testclient import TestClient
from app.models_data_base_structures.db_water_structure import Base
from app.main import app
import pytest
from sqlalchemy.orm import sessionmaker,declarative_base
from sqlalchemy import create_engine

@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c

@pytest.fixture
def test_data_for_api_check(client):    
    #default tank for tests, and it will return it
    response = client.post("/tank/create/",
                        headers={},
                        json={'tank_tag':"test_tank1",'name':'name1','capacity':10,'owner':'bob','status':0}
                        )
    assert response.status_code == 200
    return response.json()

@pytest.fixture
def db_test_session():
    # Base = declarative_base() - we need object which was used in data model
    engine = create_engine('sqlite:///:memory:',echo=False)
    Base.metadata.create_all(engine)
    Session=sessionmaker(bind=engine)
    session=Session()
    yield session
    session.close()