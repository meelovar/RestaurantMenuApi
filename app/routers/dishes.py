from typing import Mapping
from uuid import UUID

from fastapi import (
    APIRouter,
    Depends,
)
from starlette import status

from app.dependencies import (
    valid_dish,
)
from app.schemas import (
    DishSchemaIn,
    DishSchemaOut,
)
from app.services import DishesService

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
async def create(menu_id: UUID, submenu_id: UUID, dish_data: DishSchemaIn, dishes_svc: DishesService = Depends()):
    result = await dishes_svc.create(menu_id, submenu_id, dish_data)

    return result


@router.patch("/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}", response_model=DishSchemaOut)
async def update(
        menu_id: UUID,
        submenu_id: UUID,
        dish_id: UUID,
        dish_data: DishSchemaIn,
        dish_svc: DishesService = Depends()
):
    return await dish_svc.update(menu_id, submenu_id, dish_id, dish_data)


@router.delete("/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}")
async def delete(menu_id: UUID, submenu_id: UUID, dish_id: UUID, dish_svc: DishesService = Depends()):
    await dish_svc.delete(menu_id, submenu_id, dish_id)

    return {"status": True, "message": "The dish has been deleted"}
