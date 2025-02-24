"""Modelos de tablas"""

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from database import DATABASE_URL

# Sync engine para auto map
sync_engine = create_engine(DATABASE_URL.replace("mssql+aioodbc", "mssql+pyodbc"),
    connect_args={"autocommit": True})

Base = automap_base()

with sync_engine.connect() as conn:
    Base.prepare(conn, reflect=True, schema="Planning")


org_actual = Base.classes.get("ORG_ACTUAL") 
roles = Base.classes.get("ROLES")
rol_detalle = Base.classes.get("ROL_DETALLE")
dependencia = Base.classes.get("DEPENDENCIA")
grupos = Base.classes.get("GRUPOS")
personas = Base.classes.get("PERSONAS")

sync_engine.dispose()