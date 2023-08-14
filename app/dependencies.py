from uuid import UUID

from fastapi import Depends
from starlette import status
from starlette.exceptions import HTTPException

from app.models import Dish, Menu, Submenu
from app.services.dishes import DishesService
from app.services.menus import MenuService
from app.services.submenus import SubmenuService


async def valid_menu(menu_id: UUID, menu_svc: MenuService = Depends()) -> Menu:
    menu = await menu_svc.get_by_id(menu_id)

    return __raise_404_or_return(menu, 'menu not found')


async def valid_submenu(menu_id: UUID, submenu_id: UUID, submenu_svc: SubmenuService = Depends()) -> Submenu:
    submenu = await submenu_svc.get_by_id(menu_id, submenu_id)

    return __raise_404_or_return(submenu, 'submenu not found')


async def valid_dish(menu_id: UUID, submenu_id: UUID, dish_id: UUID, dish_svc: DishesService = Depends()) -> Dish:
    dish = await dish_svc.get_by_id(menu_id, submenu_id, dish_id)

    return __raise_404_or_return(dish, 'dish not found')


def __raise_404_or_return(obj, message: str):
    """Raises 404 HTTP Exception if object is None or returns it"""
    if obj is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, message)

    return obj
