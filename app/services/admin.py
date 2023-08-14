import os
from decimal import Decimal
from typing import Any
from uuid import UUID

import pandas as pd
from starlette.background import BackgroundTasks

from app.cache import RedisCache
from app.database import get_async_session_cm, get_redis_session_cm
from app.repositories import DishesRepository, MenuRepository, SubmenuRepository
from app.schemas import (
    CatalogSubmenuItemSchema,
    DishSchemaOut,
    DishSchemaXlsx,
    MenuCatalogSchemaOut,
    MenuSchemaXlsx,
    SubmenuSchemaXlsx,
)
from app.services.dishes import DishesService
from app.services.menus import CatalogService, MenuService
from app.services.submenus import SubmenuService


class AdminService:
    def __init__(self, filename: str):
        self.filename = filename
        self.db_session = get_async_session_cm
        self.redis_session = get_redis_session_cm
        self.catalog_svc_cls = CatalogService
        self.menu_svc_cls = MenuService
        self.submenu_svc_cls = SubmenuService
        self.dish_svc_cls = DishesService
        self.menu_repo = MenuRepository
        self.submenu_repo = SubmenuRepository
        self.dish_repo = DishesRepository
        self.menus_to_insert: dict[UUID, Any] = {}
        self.submenus_to_insert: dict[UUID, Any] = {}
        self.dishes_to_insert: dict[UUID, Any] = {}
        self.menus_to_update: dict[UUID, Any] = {}
        self.menus_to_delete: list[UUID] = []
        self.submenus_to_update: dict[UUID, Any] = {}
        self.submenus_to_delete: list[dict[str, UUID]] = []
        self.dishes_to_update: dict[UUID, Any] = {}
        self.dishes_to_delete: list[dict[str, UUID]] = []

    async def execute(self) -> None:
        if not os.path.exists(self.filename):
            return

        self.__process_excel()
        await self.__process_menu_catalog()
        await self.__sync_db()

    def __process_excel(self) -> None:
        catalog_df = pd.read_excel(self.filename, header=None)
        menu_slice = slice(0, 3)
        submenu_slice = slice(1, 4)
        dish_slice = slice(2, 5)
        menu_id, submenu_id = None, None

        for i, row in catalog_df.iterrows():
            if row.iloc[menu_slice].notna().all():
                menu_item = self.__process_menu_row(row)
                menu_id = menu_item['id']
            elif menu_id is not None and row.iloc[submenu_slice].notna().all():
                submenu_item = self.__process_submenu_row(row, menu_id)
                submenu_id = submenu_item['id']
            elif menu_id is not None and row.iloc[dish_slice].notna().all():
                self.__process_dish_row(row, submenu_id, menu_id)

    async def __process_menu_catalog(self) -> None:
        async with self.db_session() as db:
            async with self.redis_session() as redis:
                catalog = await self.catalog_svc_cls(self.menu_repo(db), RedisCache(redis)).get_catalog()

        for menu in catalog:
            self.__process_menu_item(menu)

    async def __sync_db(self) -> None:
        async with self.db_session() as db:
            async with self.redis_session() as redis:
                background_tasks = BackgroundTasks()
                menu_service = self.menu_svc_cls(background_tasks, self.menu_repo(db), RedisCache(redis))
                submenu_service = self.submenu_svc_cls(background_tasks, self.submenu_repo(db), RedisCache(redis))
                dish_service = self.dish_svc_cls(background_tasks, self.dish_repo(db), RedisCache(redis))

                for menu in self.menus_to_insert.values():
                    await menu_service.create(MenuSchemaXlsx(**menu))

                for submenu in self.submenus_to_insert.values():
                    await submenu_service.create(submenu['menu_id'], SubmenuSchemaXlsx(**submenu))

                for dish in self.dishes_to_insert.values():
                    await dish_service.create(dish['menu_id'], dish['submenu_id'], DishSchemaXlsx(**dish))

                for menu in self.menus_to_update.values():
                    await menu_service.update(menu['id'], MenuSchemaXlsx(**menu))

                for submenu in self.submenus_to_update.values():
                    await submenu_service.update(submenu['menu_id'], submenu['id'], SubmenuSchemaXlsx(**submenu))

                for dish in self.dishes_to_update.values():
                    await dish_service.update(dish['menu_id'], dish['submenu_id'], dish['id'], DishSchemaXlsx(**dish))

                for dish in self.dishes_to_delete:
                    await dish_service.delete(dish['menu_id'], dish['submenu_id'], dish['id'])

                for submenu in self.submenus_to_delete:
                    await submenu_service.delete(submenu['menu_id'], submenu['id'])

                for menu_id in self.menus_to_delete:
                    await menu_service.delete(menu_id)

    def __process_menu_row(self, row: pd.Series) -> dict[str, Any]:
        menu_id = UUID(row.iloc[0])
        menu_item = {
            'id': menu_id,
            'title': row.iloc[1],
            'description': row.iloc[2]
        }

        self.menus_to_insert[menu_id] = menu_item

        return menu_item

    def __process_submenu_row(self, row: pd.Series, menu_id: UUID) -> dict[str, Any]:
        submenu_id = UUID(row.iloc[1])
        submenu_item = {
            'id': submenu_id,
            'menu_id': menu_id,
            'title': row.iloc[2],
            'description': row.iloc[3]
        }

        self.submenus_to_insert[submenu_id] = submenu_item

        return submenu_item

    def __process_dish_row(self, row: pd.Series, submenu_id: Any, menu_id: Any) -> None:
        dish_id = UUID(row.iloc[2])
        dish_item = {
            'id': dish_id,
            'submenu_id': submenu_id,
            'menu_id': menu_id,
            'title': row.iloc[3],
            'description': row.iloc[4],
            'price': Decimal(row.iloc[5]),
        }

        self.dishes_to_insert[dish_id] = dish_item

    def __process_menu_item(self, item: MenuCatalogSchemaOut) -> None:
        item_id = item.id
        excel_item = self.menus_to_insert.get(item_id)

        if excel_item is None:
            self.menus_to_delete.append(item_id)
            self.menus_to_insert.pop(item_id)
        elif item.title != excel_item['title'] or item.description != excel_item['description']:
            self.menus_to_update[item_id] = self.menus_to_insert.pop(item_id)
        elif item.title == excel_item['title'] and item.description == excel_item['description']:
            self.menus_to_insert.pop(item_id)

        for submenu_item in item.submenus:
            self.__process_submenu_item(submenu_item, item.id)

    def __process_submenu_item(self, item: CatalogSubmenuItemSchema, menu_id: UUID) -> None:
        item_id = item.id
        excel_item = self.submenus_to_insert.get(item_id)

        if excel_item is None:
            self.submenus_to_delete.append({'id': item_id, 'menu_id': menu_id})
            self.submenus_to_insert.pop(item_id)
        elif item.title != excel_item['title'] or \
                item.description != excel_item['description'] or \
                menu_id != excel_item['menu_id']:
            self.submenus_to_update[item_id] = self.submenus_to_insert.pop(item_id)
        elif item.title == excel_item['title'] and \
                item.description == excel_item['description'] and \
                menu_id == excel_item['menu_id']:
            self.submenus_to_insert.pop(item_id)

        for dish_item in item.dishes:
            self.__process_dish_item(dish_item, item_id, menu_id)

    def __process_dish_item(self, item: DishSchemaOut, submenu_id: UUID, menu_id: UUID) -> None:
        item_id = item.id
        excel_item = self.dishes_to_insert.get(item_id)

        if excel_item is None:
            self.dishes_to_delete.append({'id': item_id, 'submenu_id': submenu_id, 'menu_id': menu_id})
        elif item.title != excel_item['title'] or \
                item.description != excel_item['description'] or \
                item.price != excel_item['price'] or \
                submenu_id != excel_item['submenu_id']:
            self.dishes_to_update[item_id] = self.dishes_to_insert.pop(item_id)
        elif item.title == excel_item['title'] and \
                item.description == excel_item['description'] and \
                item.price == excel_item['price'] and \
                submenu_id == excel_item['submenu_id']:
            self.dishes_to_insert.pop(item_id)
