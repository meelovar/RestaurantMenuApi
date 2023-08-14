from uuid import UUID

from fastapi import Depends
from starlette.background import BackgroundTasks

from app.cache import RedisCache
from app.models import Submenu
from app.repositories import SubmenuRepository
from app.schemas import SubmenuSchemaIn, SubmenuSchemaOut
from app.specifications import SubmenuListSpecification, SubmenuSpecification


class SubmenuService:
    def __init__(
            self,
            background_tasks: BackgroundTasks,
            repo: SubmenuRepository = Depends(),
            cache: RedisCache = Depends()
    ):
        self.__bg_tasks = background_tasks
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
        cache_keys = 'menus', f'menus:{menu_id}', f'submenus:{menu_id}', 'catalog'
        submenu = await self.__repo.create(submenu_data, menu_id)

        self.__bg_tasks.add_task(self.__cache.delete, cache_keys)

        return submenu

    async def update(self, menu_id: UUID, submenu_id: UUID, update_data: SubmenuSchemaIn) -> Submenu:
        cache_key = f'submenus:{menu_id}:{submenu_id}', f'submenus:{menu_id}', 'catalog'
        result = await self.__repo.update(SubmenuSpecification(menu_id, submenu_id), update_data)

        self.__bg_tasks.add_task(self.__cache.delete, cache_key)

        return result

    async def delete(self, menu_id: UUID, submenu_id: UUID) -> None:
        cache_keys = (
            'menus', f'menus:{menu_id}',
            f'submenus:{menu_id}', f'submenus:{menu_id}:{submenu_id}',
            f'dishes:{menu_id}:{submenu_id}*',
            'catalog'
        )

        await self.__repo.delete(SubmenuSpecification(menu_id, submenu_id))
        self.__bg_tasks.add_task(self.__cache.delete, cache_keys)
