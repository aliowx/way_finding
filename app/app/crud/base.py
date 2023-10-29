from datetime import datetime
from typing import Awaitable, Any, Generic, Type, TypeVar, Sequence

from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import func, Row, RowMapping
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import exc

from app.db.base_class import Base


ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).

        **Parameters**

        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model

    async def get(self, db: AsyncSession, id: int | str) -> Awaitable[ModelType | None]:
        query = select(self.model).where(self.model.id == id)
        response = await db.execute(query)
        return response.scalar_one_or_none()

    async def get_by_ids(
        self, db: AsyncSession, list_ids: list[int | str]
    ) -> Sequence[Row | RowMapping | Any]:
        query = select(self.model).where(self.model.id.in_(list_ids))
        response = await db.execute(query)
        return response.scalars().all()

    async def get_count(self, db: AsyncSession) -> Awaitable[ModelType | None]:
        query = select(func.count()).select_from(select(self.model).subquery())
        response = await db.execute(query)
        return response.scalar_one()

    async def get_multi(
        self, db: AsyncSession, skip: int = 0, limit: int = 100
    ) -> Sequence[Row | RowMapping | Any]:
        query = select(self.model).offset(skip).limit(limit).order_by(self.model.id)
        response = await db.execute(query)
        return response.scalars().all()

    async def get_multi_ordered(
        self,
        db: AsyncSession,
        skip: int = 0,
        limit: int | None = 100,
        order_by: list = None,
    ) -> Sequence[Row | RowMapping | Any]:
        if order_by is None:
            order_by = []
        order_by.append(self.model.id.asc())

        query = select(self.model).order_by(*order_by).offset(skip)
        if limit is None:
            response = await db.execute(query)
            return response.scalars().all()
        response = await db.execute(query.limit(limit))
        return response.scalars().all()

    async def create(
        self, db: AsyncSession, obj_in: CreateSchemaType | dict
    ) -> Awaitable[ModelType]:
        if not isinstance(obj_in, dict):
            obj_in = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in)  # type: ignore
        try:
            db.add(db_obj)
            await db.commit()
        except exc.IntegrityError:
            await db.rollback()
            raise HTTPException(
                status_code=409,
                detail="Resource already exists",
            )
        await db.refresh(db_obj)
        return db_obj

    async def update(
            self,
            db: AsyncSession,
            db_obj: ModelType,
            obj_in: UpdateSchemaType | dict[str, Any] | ModelType
    ) -> Awaitable[ModelType]:
        if obj_in is not None:
            obj_data = jsonable_encoder(db_obj)
            if isinstance(obj_in, dict):
                update_data = obj_in
            else:
                update_data = obj_in.model_dump(exclude_unset=True)
            for field in obj_data:
                if field in update_data:
                    setattr(db_obj, field, update_data[field])
        if hasattr(self.model, "modified"):
            setattr(db_obj, "modified", datetime.now())
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def remove(self, db: AsyncSession, *, id: int | str) -> Awaitable[ModelType]:
        query = select(self.model).where(self.model.id == id)
        response = await db.execute(query)
        obj = response.scalar_one()
        await db.delete(obj)
        await db.commit()
        return obj
