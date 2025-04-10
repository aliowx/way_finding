import pandas as pd
from app import schemas, crud
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from app.api import deps
from app.db.session import async_session
from app import exceptions as exc
from app.crud.crud_vertex import vertex

df = pd.read_csv('data1.csv')

async def data(
    *,
    vertex_in: schemas.VertexCreate,
):
    vertex_list = []  
    failed_insertions = []
    async with async_session() as db:
        crud.vertex.get(db=db)
        
        for index, row in df.iterrows():
            vertex = crud.vertex.model(
                x = row[''],
                y = row['']
            )
            
            vertex_list.append(vertex)

            if len(vertex_list) == 100:
                try:
                    db.add_all(vertex_list)
                    await db.commit()
                    vertex_list = []

                except Exception as ex:
                    await db.rollback()
                    failed_insertions.append(vertex_list)
                    vertex_list = []    
    if vertex_list:
        try:
            db.add_all(vertex_list)
            await db.commit()
        except Exception as ex:
            await db.rollback()
            failed_insertions.extend(vertex_list)

    for vertex in failed_insertions:
        try:
            db.add(vertex)
            await db.commit()
        except Exception as ex:
            await db.rollback()