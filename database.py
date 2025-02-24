"""Conexión a DB"""

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import urllib


DB_SERVER = "10.150.6.5"  
DB_NAME = "DevPctPncOsop"
DB_USER = "api.pctpncosop.planning"
DB_PASSWORD = "R^y7&Nec=OLZ]J4M5k.q"

DATABASE_URL = (
    f"mssql+aioodbc://{DB_USER}:{DB_PASSWORD}@{DB_SERVER}/{DB_NAME}"
    f"?driver=ODBC+Driver+17+for+SQL+Server"
)

# Crear variable de async engine
engine = create_async_engine(DATABASE_URL, echo=True, future=True, connect_args={"autocommit": True})

# Session con async
SessionLocal = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

Base = declarative_base()

# Función 
async def get_db():
    async with SessionLocal() as session:
        yield session