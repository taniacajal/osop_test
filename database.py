"""Conexión a DB"""

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import urllib


DB_SERVER = "10.88.0.138"  
DB_NAME = "OSOP2"
DB_USER = "test_ext"
DB_PASSWORD = "Temporal_MJSP_2025"
DB_SCHEMA = "esquemavista"  

DATABASE_URL = (
    f"mssql+aioodbc://{DB_USER}:{DB_PASSWORD}@{DB_SERVER}/{DB_NAME}"
    f"?driver=ODBC+Driver+17+for+SQL+Server&CurrentSchema={DB_SCHEMA}"
)

# Crear variable de async engine
engine = create_async_engine(DATABASE_URL, echo=True, future=True)

# Session con async
SessionLocal = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

Base = declarative_base()

# Función 
async def get_db():
    async with SessionLocal() as session:
        yield session