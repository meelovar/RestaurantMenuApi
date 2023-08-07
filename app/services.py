from uuid import UUID

from fastapi import Depends

from app.cache import RedisCache
from app.models import Dish, Menu, Submenu
from app.repositories import DishesRepository, MenuRepository, SubmenuRepository
from app.schemas import (
    DishSchemaIn,
    DishSchemaOut,
    MenuSchemaIn,
    MenuSchemaOut,
    SubmenuSchemaIn,
    SubmenuSchemaOut,
)
from app.specifications import (
    DishListSpecification,
    DishSpecification,
    MenuSpecification,
    SubmenuListSpecification,
    SubmenuSpecification,
)


class MenuService:
    def __init__(self, repo: MenuRepository = Depends(), cache: RedisCache = Depends()):
        self.__repo = repo
        self.__cache = cache

    async def get_by_id(self, menu_id: UUID) -> Menu | MenuSchemaOut | None:
        cache_key = f'menus:{menu_id}'
        cached = await self.__cache.get(cache_key)

        if not cached:
            result = await self.__repo.get(MenuSpecification(menu_id))

            await self.__cache.set(cache_key, result)
        else:
            result = MenuSchemaOut.model_validate(cached)

        return result

    async def get_list(self) -> list[Menu | MenuSchemaOut]:
        cache_key = 'menus'
        cached = await self.__cache.get(cache_key)

        if not cached:
            result = await self.__repo.get_list()

            await self.__cache.set(cache_key, result)
        else:
            result = list(map(MenuSchemaOut.model_validate, cached))

        return result

    async def create(self, menu_data: MenuSchemaIn) -> Menu:
        cache_key = 'menus'
        menu = await self.__repo.create(menu_data)

        await self.__cache.delete(cache_key)

        return menu

    async def update(self, menu_id: UUID, update_data: MenuSchemaIn) -> Menu:
        cache_keys = 'menus', f'menus:{menu_id}'
        result = await self.__repo.update(MenuSpecification(menu_id), update_data)

        await self.__cache.delete(*cache_keys)

        return result

    async def delete(self, menu_id: UUID) -> None:
        cache_keys = 'menus', f'menus:{menu_id}'

        await self.__repo.delete(MenuSpecification(menu_id))
        await self.__cache.delete(*cache_keys)


class SubmenuService:
    def __init__(self, repo: SubmenuRepository = Depends(), cache: RedisCache = Depends()):
        self.__repo = repo
        self.__cache = cache

    async def get_by_id(self, menu_id: UUID, submenu_id: UUID) -> Submenu | SubmenuSchemaOut | None:
        cache_key = f'submenus:{menu_id}:{submenu_id}'
        cached = await self.__cache.get(cache_key)

        if not cached:
            result = await self.__repo.get(SubmenuSpecification(menu_id, submenu_id))

            await self.__cache.set(cache_key, result)
        else:
            result = SubmenuSchemaOut.model_validate(cached)

        return result

    async def get_list(self, menu_id: UUID) -> list[Submenu | SubmenuSchemaOut]:
        cache_key = f'submenus:{menu_id}'
        cached = await self.__cache.get(cache_key)

        if not cached:
            result = await self.__repo.get_list(SubmenuListSpecification(menu_id))

            await self.__cache.set(cache_key, result)
        else:
            result = list(map(SubmenuSchemaOut.model_validate, cached))

        return result

    async def create(self, menu_id: UUID, submenu_data: SubmenuSchemaIn) -> Submenu:
        cache_keys = 'menus*', f'submenus:{menu_id}'
        submenu = await self.__repo.create(submenu_data, menu_id)

        await self.__cache.delete(*cache_keys)

        return submenu

    async def update(self, menu_id: UUID, submenu_id: UUID, update_data: SubmenuSchemaIn) -> Submenu:
        cache_key = f'submenus:{menu_id}:{submenu_id}', f'submenus:{menu_id}'
        result = await self.__repo.update(SubmenuSpecification(menu_id, submenu_id), update_data)

        await self.__cache.delete(*cache_key)

        return result

    async def delete(self, menu_id: UUID, submenu_id: UUID) -> None:
        cache_keys = 'menus*', f'menus:{menu_id}', f'submenus:{menu_id}*'

        await self.__repo.delete(SubmenuSpecification(menu_id, submenu_id))
        await self.__cache.delete(*cache_keys)


class DishesService:
    def __init__(self, repo: DishesRepository = Depends(), cache: RedisCache = Depends()):
        self.__repo = repo
        self.__cache = cache

    async def get_by_id(self, menu_id: UUID, submenu_id: UUID, dish_id: UUID) -> Dish | DishSchemaOut | None:
        cache_key = f'dishes:{menu_id}:{submenu_id}:{dish_id}'
        cached = await self.__cache.get(cache_key)

        if not cached:
            result = await self.__repo.get(DishSpecification(menu_id, submenu_id, dish_id))

            await self.__cache.set(cache_key, result)
        else:
            result = DishSchemaOut.model_validate(cached)

        return result

    async def get_list(self, menu_id: UUID, submenu_id: UUID) -> list[Dish | DishSchemaOut]:
        cache_key = f'dishes:{menu_id}:{submenu_id}'
        cached = await self.__cache.get(cache_key)

        if not cached:
            result = await self.__repo.get_list(DishListSpecification(menu_id, submenu_id))

            await self.__cache.set(cache_key, result)
        else:
            result = list(map(DishSchemaOut.model_validate, cached))

        return result

    async def create(self, menu_id: UUID, submenu_id: UUID, dish_data: DishSchemaIn) -> Dish:
        cache_key = 'menus', f'menus:{menu_id}', f'submenus:{menu_id}', f'submenus:{menu_id}:{submenu_id}'
        dish = await self.__repo.create(dish_data, submenu_id)

        await self.__cache.delete(*cache_key)

        return dish

    async def update(self, menu_id: UUID, submenu_id: UUID, dish_id: UUID, update_data: DishSchemaIn) -> Dish:
        cache_keys = f'submenus:{menu_id}:{submenu_id}', f'dishes:{menu_id}:{submenu_id}:{dish_id}'
        result = await self.__repo.update(DishSpecification(menu_id, submenu_id, dish_id), update_data)

        await self.__cache.delete(*cache_keys)

        return result

    async def delete(self, menu_id: UUID, submenu_id: UUID, dish_id: UUID) -> None:
        cache_keys = (
            'menus', f'menus:{menu_id}',
            f'submenus:{menu_id}', f'submenus:{menu_id}:{submenu_id}',
            f'dishes:{menu_id}:{submenu_id}', f'dishes:{menu_id}:{submenu_id}:{dish_id}'
        )

        await self.__repo.delete(DishSpecification(menu_id, submenu_id, dish_id))
        await self.__cache.delete(*cache_keys)
