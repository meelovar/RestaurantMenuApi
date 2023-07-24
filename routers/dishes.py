from typing import Mapping
from uuid import UUID

from fastapi import (
    APIRouter,
    Depends,
)
from starlette import status

from dependencies import (
    valid_dish,
    valid_submenu,
)
from models import Submenu
from schemas import (
    DishSchemaIn,
    DishSchemaOut,
)
from services import DishesService

router = APIRouter(prefix="/menus", tags=["dishes"])


@router.get("/{menu_id}/submenus/{submenu_id}/dishes", response_model=list[DishSchemaOut])
async def get_list(menu_id: UUID, submenu_id: UUID, dishes_svc: DishesService = Depends()):
    result = await dishes_svc.get_list(menu_id, submenu_id)

    return result


@router.get("/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}", response_model=DishSchemaOut)
async def get(dish: Mapping = Depends(valid_dish)):
    return dish


@router.post("/{menu_id}/submenus/{submenu_id}/dishes",
             response_model=DishSchemaOut,
             status_code=status.HTTP_201_CREATED)
async def create(dish_data: DishSchemaIn,
                 submenu: Submenu = Depends(valid_submenu),
                 dishes_svc: DishesService = Depends()):
    result = await dishes_svc.create(submenu.id, dish_data)

    return result


@router.patch("/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}", response_model=DishSchemaOut)
async def update(dish_data: DishSchemaIn,
                 dish: Mapping = Depends(valid_dish),
                 dish_svc: DishesService = Depends()):
    return await dish_svc.update(dish, dish_data)


@router.delete("/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}")
async def delete(dish: Mapping = Depends(valid_dish), dish_svc: DishesService = Depends()):
    await dish_svc.delete(dish)

    return {"status": True, "message": "The dish has been deleted"}
