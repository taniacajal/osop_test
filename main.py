from fastapi import FastAPI, Depends, HTTPException, status, Query
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.responses import FileResponse
from passlib.context import CryptContext
import jwt
import uvicorn
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from database import get_db
from dependencies import get_id_delegacion  # ✅ Filtro por delegación
from models import org_actual, roles, rol_detalle, dependencia, grupos, personas
from datetime import datetime, timedelta

# Clave secreta para firmar los tokens
SECRET_KEY = "superclaveultrasegura"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

app = FastAPI()

# Base de datos simulada de usuarios
fake_users_db = {
    "usuario1": {
        "username": "usuario1",
        "full_name": "Usuario Ejemplo",
        "email": "usuario1@example.com",
        "hashed_password": "$2b$12$igCfpBXV8.aCJf3Vj2yqLO/iwyv7AHFP3FqzJYPVsJF/TZpp/XGvy",  # "12345"
    }
}

# Configuración de hash de contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Configuración de OAuth2 para el token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Función para verificar contraseña
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


# Función para obtener usuario simulado
def get_user(username: str):
    user = fake_users_db.get(username)
    if user:
        return user
    return None


# Función para autenticar usuario
def authenticate_user(username: str, password: str):
    user = get_user(username)
    if not user or not verify_password(password, user["hashed_password"]):
        return None
    return user


# Función para crear un token JWT
def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# Endpoint de login para obtener token
@app.post("/token")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["username"]}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}


# Función para obtener usuario desde el token
def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Token inválido")
        return get_user(username)
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expirado")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Token inválido")

#---------------------------------------

@app.get("/planilla")
async def get_planilla(
    iddelegacion: int = Depends(get_id_delegacion),  # ✅ Filtrado
    db: AsyncSession = Depends(get_db),
    #current_user: dict = Depends(get_current_user) 
):
    async with db.begin():
        result = await db.execute(select(org_actual).where(org_actual.id_delegacion == iddelegacion))
        planilla = result.scalars().all()
    
    return {"planilla": [e.__dict__ for e in planilla]}  # JSON


@app.get("/roles")
async def get_shifts(
    db: AsyncSession = Depends(get_db),
    #current_user: dict = Depends(get_current_user)
):
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

if __name__ == '__main__':
  uvicorn.run(app, host="0.0.0.0", port=8500)