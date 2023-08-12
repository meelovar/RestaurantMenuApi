from uuid import UUID

from fastapi import Depends

from app.cache import RedisCache
from app.models import Dish
from app.repositories import DishesRepository
from app.schemas import DishSchemaIn, DishSchemaOut
from app.specifications import DishDeleteUpdateSpecification, DishListSpecification, DishSpecification


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
        cache_keys = f'dishes:{menu_id}:{submenu_id}', f'dishes:{menu_id}:{submenu_id}:{dish_id}'
        result = await self.__repo.update(DishDeleteUpdateSpecification(menu_id, submenu_id, dish_id), update_data)

        await self.__cache.delete(*cache_keys)

        return result

    async def delete(self, menu_id: UUID, submenu_id: UUID, dish_id: UUID) -> None:
        cache_keys = (
            'menus', f'menus:{menu_id}',
            f'submenus:{menu_id}', f'submenus:{menu_id}:{submenu_id}',
            f'dishes:{menu_id}:{submenu_id}', f'dishes:{menu_id}:{submenu_id}:{dish_id}'
        )

        await self.__repo.delete(DishDeleteUpdateSpecification(menu_id, submenu_id, dish_id))
        await self.__cache.delete(*cache_keys)
