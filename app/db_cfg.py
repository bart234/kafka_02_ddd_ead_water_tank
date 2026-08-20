from dotenv import load_dotenv
from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
import os

#path loading from env
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./default.db")

engine = create_engine(DATABASE_URL,echo=True)

Base = declarative_base()
Base.metadata.create_all(engine)
