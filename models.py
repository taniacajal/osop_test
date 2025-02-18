"""Modelos de tablas"""

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from database import DATABASE_URL

# Sync engine para auto map
sync_engine = create_engine(DATABASE_URL.replace("mssql+aioodbc", "mssql+pyodbc"))
Base = automap_base()

# Reflejar tablas
with sync_engine.connect() as conn:
    Base.prepare(conn, reflect=True)

org_actual = Base.classes.ORG_ACTUAL  
sync_engine.dispose()