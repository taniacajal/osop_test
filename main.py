from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from database import get_db
from dependencies import get_id_delegacion  # ✅ Filtro por delegación
from models import org_actual

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
