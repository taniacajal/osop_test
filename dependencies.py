"""Dependencias"""

from fastapi import Header, HTTPException, Request

# Extraer id delegacion de headers
def get_id_delegacion(request : Request, id_delegacion: int = Header(None)):
    print("Received headers:", request.headers)
    if id_delegacion is None:
        raise HTTPException(status_code=400, detail="id_delegacion es requerido en encabezado")
    return id_delegacion

