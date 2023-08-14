from uuid import UUID

from fastapi import Depends
from pydantic import TypeAdapter

from app.cache import RedisCache
from app.models import Menu
from app.repositories import MenuRepository
from app.schemas import MenuCatalogSchemaOut, MenuSchemaIn, MenuSchemaOut
from app.specifications import MenuSpecification


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
        cache_keys = 'menus', f'menus:{menu_id}', f'submenus:{menu_id}*', f'dishes:{menu_id}*'

        await self.__repo.delete(MenuSpecification(menu_id))
        await self.__cache.delete(*cache_keys)


class CatalogService:
    def __init__(self, repo: MenuRepository = Depends(), cache: RedisCache = Depends()):
        self.__repo = repo
        self.__cache = cache

    async def get_catalog(self):
        result = await self.__repo.get_catalog()
        adapter = TypeAdapter(list[MenuCatalogSchemaOut])

        return adapter.validate_python(result)
