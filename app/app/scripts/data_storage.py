import pandas as pd
import logging
import asyncio
from app import crud
from app.db.session import async_session
from app.schemas.vertex import VertexCreate

df = pd.read_csv('vertex.csv')
logger = logging.getLogger()

async def save_vertex():

    vertex_list = []  
    failed_insertions = []

    for index, row in df.iterrows():

        vertex = VertexCreate(
            endx = (row['endx']),
            endy = (row['endy']),
            startx = (row['startx']),
            starty = (row['starty']),
            pox = (row['pox']),
            poy = (row['poy'])  
        )
        vertex_list.append(vertex)  

        async with async_session() as db:        
            if len(vertex_list) == 100:
                try:
                    await crud.vertex.create_multi(db,vertex_list)
                    await db.commit()
                    logger.info('Data inserted successfully')
                    vertex_list = []

                except Exception as ex:
                    failed_insertions.append(vertex_list)
                    vertex_list = []   
    if vertex_list:
        try:
            await crud.vertex.create_multi(db,vertex_list)
        except Exception as ex:
            failed_insertions.extend(vertex_list)

    fail = [] 
    for vertex in failed_insertions:
        try:
            db.add(vertex)
            await db.commit()
        except Exception as ex:
            await db.rollback()
    logger.info(f'This file was fail{fail}')
    
if __name__== "__main__":
    asyncio.run(save_vertex())