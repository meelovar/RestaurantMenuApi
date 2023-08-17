import abc
import uuid
from typing import Generic, TypeVar

import pydantic
from fastapi import Depends
from sqlalchemy import Result, ScalarResult, Select, delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.database import get_async_session
from app.models import BaseModel, Dish, Menu, Submenu
from app.specifications import SpecificationBase

ModelT = TypeVar('ModelT', bound=BaseModel)


class RepositoryBase(Generic[ModelT], metaclass=abc.ABCMeta):
    def __init__(self, session: AsyncSession = Depends(get_async_session)):
        self._session = session

    async def get(self, spec: SpecificationBase) -> ModelT | None:
        result = (await self._do_get(spec)).scalar_one_or_none()

        return result

    async def get_list(self, spec: SpecificationBase | None = None) -> list[ModelT]:
        query = self._get_select_query()

        if spec:
            query = query.where(spec.execute())

        result = (await self._session.execute(query)).scalars()

        return [r for r in result]

    async def create(self, data: pydantic.BaseModel, relation_id: uuid.UUID | None = None) -> ModelT:
        obj = self._do_create(data, relation_id)

        self._session.add(obj)

        await self._session.commit()
        await self._session.refresh(obj)

        return obj

    async def update(self, spec: SpecificationBase, data: pydantic.BaseModel) -> ModelT:
        query = update(self._model_cls).values(data.model_dump(exclude_unset=True)).where(spec.execute())

        await self._session.execute(query)
        await self._session.commit()

        return (await self._do_get(spec)).scalar_one()

    async def delete(self, spec: SpecificationBase) -> None:
        query = delete(self._model_cls).where(spec.execute())

        await self._session.execute(query)
        await self._session.commit()

    _model_cls: type[ModelT]

    async def _do_get(self, spec: SpecificationBase) -> Result:
        query = self._get_select_query().where(spec.execute())
        result = await self._session.execute(query)

        return result

    @abc.abstractmethod
    def _do_create(self, data: pydantic.BaseModel, relation_id: uuid.UUID | None) -> ModelT:
        pass

    def _get_select_query(self) -> Select:
        return select(self._model_cls)


class MenuRepository(RepositoryBase[Menu]):
    async def get_catalog(self) -> ScalarResult:
        query = self._get_select_query().options(joinedload(self._model_cls.submenus).joinedload(Submenu.dishes))
        result = (await self._session.execute(query)).unique().scalars()

        return result

    def _do_create(self, data: pydantic.BaseModel, relation_id: uuid.UUID | None) -> Menu:
        menu = self._model_cls(**data.model_dump())

        return menu

    _model_cls = Menu


class SubmenuRepository(RepositoryBase[Submenu]):
    _model_cls = Submenu

    def _do_create(self, data: pydantic.BaseModel, relation_id: uuid.UUID | None) -> Submenu:
        submenu = self._model_cls(**data.model_dump())

        submenu.menu_id = relation_id

        return submenu


class DishesRepository(RepositoryBase[Dish]):
    _model_cls = Dish

    def _do_create(self, data: pydantic.BaseModel, relation_id: uuid.UUID | None) -> Dish:
        dish = self._model_cls(**data.model_dump())

        dish.submenu_id = relation_id

        return dish

    def _get_select_query(self) -> Select:
        return super()._get_select_query().join(Submenu)
