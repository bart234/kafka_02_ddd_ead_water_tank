from fastapi import FastAPI
from app.models_data_base_structures.db_water_structure import Base
from app.db_cfg import engine
from app.api.routers import tank_path

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(tank_path.router)

@app.get("/")
def main():
    return {"msg":"bob"}

#uvicorn main:app --reload