from uuid import UUID

from fastapi import Depends

from app.models import (
    Dish,
    Menu,
    Submenu,
)
from app.repositories import (
    DishesRepository,
    MenuRepository,
    SubmenuRepository,
)
from app.schemas import (
    DishSchemaIn,
    MenuSchemaIn,
    SubmenuSchemaIn,
)


class MenuService:
    def __init__(self, repo: MenuRepository = Depends()):
        self.__repo = repo

    async def get_by_id(self, menu_id: UUID):
        return await self.__repo.get_by_id(menu_id)

    async def get_list(self):
        return await self.__repo.get_list()

    async def create(self, menu_data: MenuSchemaIn):
        return await self.__repo.create(menu_data)

    async def update(self, menu: Menu, update_data: MenuSchemaIn):
        return await self.__repo.update(menu, update_data)

    async def delete(self, menu: Menu):
        return await self.__repo.delete(menu)


class SubmenuService:
    def __init__(self, repo: SubmenuRepository = Depends()):
        self.__repo = repo

    async def get_by_id(self, menu_id: UUID, submenu_id: UUID):
        return await self.__repo.get_by_id(menu_id, submenu_id)

    async def get_list(self, menu_id: UUID):
        return await self.__repo.get_list(menu_id)

    async def create(self, menu_id: UUID, submenu_data: SubmenuSchemaIn):
        return await self.__repo.create(menu_id, submenu_data)

    async def update(self, submenu: Submenu, update_data: SubmenuSchemaIn):
        return await self.__repo.update(submenu, update_data)

    async def delete(self, submenu: Submenu):
        return await self.__repo.delete(submenu)


class DishesService:
    def __init__(self, repo: DishesRepository = Depends()):
        self.__repo = repo

    async def get_by_id(self, menu_id: UUID, submenu_id: UUID, dish_id: UUID):
        return await self.__repo.get_by_id(menu_id, submenu_id, dish_id)

    async def get_list(self, menu_id: UUID, submenu_id: UUID):
        return await self.__repo.get_list(menu_id, submenu_id)

    async def create(self, submenu_id: UUID, dish_data: DishSchemaIn):
        return await self.__repo.create(submenu_id, dish_data)

    async def update(self, dish: Dish, update_data: DishSchemaIn):
        return await self.__repo.update(dish, update_data)

    async def delete(self, dish: Dish):
        return await self.__repo.delete(dish)
