from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from database import get_db
from dependencies import get_id_delegacion  # ✅ Filtro por delegación
from models import org_actual, roles, rol_detalle, dependencia, grupos, personas
from datetime import datetime

app = FastAPI()

@app.get("/planilla")
async def get_planilla(
    iddelegacion: int = Depends(get_id_delegacion),  # ✅ Filtrado
    db: AsyncSession = Depends(get_db)       # ✅ Injection
):
    async with db.begin():
        result = await db.execute(select(org_actual).where(org_actual.id_delegacion == iddelegacion))
        planilla = result.scalars().all()
    
    return {"planilla": [e.__dict__ for e in planilla]}  # JSON


@app.get("/roles")
async def get_shifts(db: AsyncSession = Depends(get_db)):
    async with db.begin():
        
        result = await db.execute(select(roles))
        rol = result.scalars().all()

    response = []
    for shift in rol:
        response.append({
            "Id": shift.Id,
            "Año": shift.fecha_inicio.year if shift.fecha_inicio else None,
            "Mes": shift.fecha_inicio.month if shift.fecha_inicio else None,
            "Grupo": shift.id_grupo,
            "Período": f"{shift.fecha_inicio} - {shift.fecha_fin}" if shift.fecha_inicio and shift.fecha_fin else None,
            "Delegación": "Delegación San Salvador Poniente",  # Constant value for all records
            "Fecha creación": shift.fecha_creacion
        })

    return {"shifts": response}


@app.get("/rol_agente")
async def get_rol_agente(
    iddelegacion: int = Depends(get_id_delegacion), 
    db: AsyncSession = Depends(get_db),       
):
    async with db.begin():

        result_roles = await db.execute(select(roles))
        roles = result_roles.scalars().all()

        result_rol_detalle = await db.execute(select(rol_detalle))
        rol_detalle = result_rol_detalle.scalars().all()

        result_org_actual = await db.execute(select(org_actual).where(org_actual.id_delegacion == iddelegacion))
        org_actual = result_org_actual.scalars().all()

        result_personas = await db.execute(select(personas))
        personas = result_personas.scalars().all()


