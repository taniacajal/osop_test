"""Funciones auxiliares"""

import pandas as pd 

#------------------------------------------------
#                 /rol_agente
#------------------------------------------------

def visualizar_rol_agente(rol_selection : list, roles : pd.DataFrame, rol_detalle : pd.DataFrame, org_actual : pd.DataFrame, personas : pd.DataFrame):
    
    """Esta función genera la visualización de agentes con sus roles para el ciclo seleccionado.
    Parámetros:
    - rol_selection : list (una lista con uno o más id_rol)
    Asume que los siguientes dataframes existen:
    roles, rol_detalle, org_actual, personas"""

    # Filtrar para no cargar todo el detalle de roles (se puede optimizar) + pivot 
    detalle_filtrado = rol_detalle[rol_detalle['id_rol'].isin(rol_selection)].pivot(
        index='id_rol',
        columns='dia_ciclo',
        values='id_horario'
    )

    # Mapa de grupos
    grupo_rol_map = dict()

    for i in rol_selection:
        grupo_i = roles[roles['Id']==i]['id_grupo'].values[0]
        grupo_rol_map[grupo_i] = i

    # Seleccionar campos esenciales de org_actual
    base = org_actual[['id_personas','nombre_grupo','nombre_conjunto']]
    base['id_rol'] = base['nombre_grupo'].map(grupo_rol_map)
    base.dropna(subset=['id_rol'], inplace=True)

    # Personas incluidas 
    personas_selection = list(base['id_personas'])

    # Unión con personas
    df = base.merge(
        personas[personas['Id'].isin(personas_selection)][['Id', 'jerarquia', 'oni', 'nombre']],
        left_on='id_personas',
        right_on='Id',
        how='left')
    
    # Mapa de líder
    df['Líder'] = df['jerarquia'].map(
        {
            "AGENTE":0,
            "CABO":1,
            "SARGENTO":1
        }
    )

    df.rename(columns={
        'nombre_grupo':'Grupo',
        'nombre_conjunto':'Conjunto',
        'jerarquia':'Categoría',
        'oni':'ONI',
        'nombre':'Nombre'
    }, inplace=True)

    df = df[['Líder','Categoría','ONI','Nombre','Conjunto','id_rol']]

    result = df.merge(detalle_filtrado, left_on='id_rol', right_on='id_rol', how='left')
    result.drop(columns=['id_rol'], inplace=True)

    return result