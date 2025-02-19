"""Dependencias"""

from fastapi import Header, HTTPException, Request

# Extraer id delegacion de headers
def get_id_delegacion(request : Request, iddelegacion: int = Header(None)):
    print("Received headers:", request.headers)
    if iddelegacion is None:
        raise HTTPException(status_code=400, detail="id_delegacion es requerido en encabezado")
    return iddelegacion

