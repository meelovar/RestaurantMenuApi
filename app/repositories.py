import uuid

from fastapi import Depends
from sqlalchemy import (
    delete,
    select,
    update,
)
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_async_session
from app.models import (
    Dish,
    Menu,
    Submenu,
)
from app.schemas import (
    DishSchemaIn,
    MenuSchemaIn,
    SubmenuSchemaIn,
)


class MenuRepository:
    def __init__(self, session: AsyncSession = Depends(get_async_session)):
        self._session = session

    async def get_by_id(self, menu_id: uuid.UUID) -> Menu | None:
        query = select(Menu).where(Menu.id == menu_id)
        result = (await self._session.execute(query)).scalar_one_or_none()

        return result

    async def get_list(self):
        query = select(Menu)
        menus = (await self._session.execute(query)).scalars()

        return menus

    async def create(self, menu_data: MenuSchemaIn) -> Menu:
        menu_obj = Menu(**menu_data.model_dump())

        self._session.add(menu_obj)

        await self._session.commit()
        await self._session.refresh(menu_obj)

        return menu_obj

    async def update(self, obj, obj_data):
        query = update(Menu).values(obj_data.model_dump(exclude_unset=True)).where(
            Menu.id == obj.id
        )

        await self._session.execute(query)
        await self._session.commit()
        await self._session.refresh(obj)

        return obj

    async def delete(self, obj):
        query = delete(Menu).where(Menu.id == obj.id)

        await self._session.execute(query)
        await self._session.commit()


class SubmenuRepository:
    def __init__(self, session: AsyncSession = Depends(get_async_session)):
        self._session = session

    async def get_by_id(self, menu_id: uuid.UUID, submenu_id: uuid.UUID) -> Submenu | None:
        query = select(Submenu).where(Submenu.menu_id == menu_id, Submenu.id == submenu_id)
        result = (await self._session.execute(query)).scalar_one_or_none()

        return result

    async def get_list(self, menu_id: uuid.UUID):
        query = select(Submenu).where(Submenu.menu_id == menu_id)
        submenus = (await self._session.execute(query)).scalars()

        return submenus

    async def create(self, menu_id: uuid.UUID, submenu_data: SubmenuSchemaIn):
        submenu = Submenu(**submenu_data.model_dump())

        submenu.menu_id = menu_id

        self._session.add(submenu)

        await self._session.commit()
        await self._session.refresh(submenu)

        return submenu

    async def update(self, obj, obj_data):
        query = update(Submenu).values(obj_data.model_dump(exclude_unset=True)).where(
            Submenu.id == obj.id
        )

        await self._session.execute(query)
        await self._session.commit()
        await self._session.refresh(obj)

        return obj

    async def delete(self, obj):
        query = delete(Submenu).where(Submenu.id == obj.id)

        await self._session.execute(query)
        await self._session.commit()


class DishesRepository:
    def __init__(self, session: AsyncSession = Depends(get_async_session)):
        self._session = session

    async def get_by_id(self, menu_id, submenu_id, dish_id):
        query = select(Dish).join(Submenu).where(
            Submenu.id == submenu_id,
            Submenu.menu_id == menu_id,
            Dish.id == dish_id
        )
        result = (await self._session.execute(query)).scalar_one_or_none()

        return result

    async def get_list(self, menu_id: uuid.UUID, submenu_id: uuid.UUID):
        query = select(Dish).join(Submenu).where(Submenu.id == submenu_id, Submenu.menu_id == menu_id)
        dishes = (await self._session.execute(query)).scalars()

        return dishes

    async def create(self, submenu_id: uuid.UUID, dish_data: DishSchemaIn):
        dish = Dish(**dish_data.model_dump())

        dish.submenu_id = submenu_id

        self._session.add(dish)

        await self._session.commit()
        await self._session.refresh(dish)

        return dish

    async def update(self, obj, obj_data):
        query = update(Dish).values(obj_data.model_dump(exclude_unset=True)).where(
            Dish.id == obj.id
        )

        await self._session.execute(query)
        await self._session.commit()
        await self._session.refresh(obj)

        return obj

    async def delete(self, obj):
        query = delete(Dish).where(Dish.id == obj.id)

        await self._session.execute(query)
        await self._session.commit()
