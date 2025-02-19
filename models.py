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
    Base.prepare(conn, reflect=True, schema="esquemavista")

# Get table reference
org_actual = Base.classes.get("ORG_ACTUAL") 
roles = Base.classes.get("ROLES")

sync_engine.dispose()