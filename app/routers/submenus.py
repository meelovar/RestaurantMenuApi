from typing import Mapping
from uuid import UUID

from fastapi import (
    APIRouter,
    Depends,
)
from starlette import status

from app.dependencies import (
    valid_menu,
    valid_submenu,
)
from app.models import Menu
from app.schemas import (
    SubmenuSchemaIn,
    SubmenuSchemaOut,
)
from app.services import SubmenuService

router = APIRouter(prefix="/menus", tags=["submenus"])


@router.get("/{menu_id}/submenus", response_model=list[SubmenuSchemaOut])
async def get_list(menu_id: UUID, submenu_svc: SubmenuService = Depends()):
    return await submenu_svc.get_list(menu_id)


@router.get("/{menu_id}/submenus/{submenu_id}", response_model=SubmenuSchemaOut)
async def get(submenu: Mapping = Depends(valid_submenu)):
    return submenu


@router.post("/{menu_id}/submenus", response_model=SubmenuSchemaOut, status_code=status.HTTP_201_CREATED)
async def create(submenu_data: SubmenuSchemaIn,
                 menu: Menu = Depends(valid_menu),
                 submenu_svc: SubmenuService = Depends()):
    return await submenu_svc.create(menu.id, submenu_data)


@router.patch("/{menu_id}/submenus/{submenu_id}", response_model=SubmenuSchemaOut)
async def update(submenu_data: SubmenuSchemaIn,
                 submenu: Mapping = Depends(valid_submenu),
                 submenu_svc: SubmenuService = Depends()):
    return await submenu_svc.update(submenu, submenu_data)


@router.delete("/{menu_id}/submenus/{submenu_id}")
async def delete(submenu: Mapping = Depends(valid_submenu), submenu_svc: SubmenuService = Depends()):
    await submenu_svc.delete(submenu)

    return {"status": True, "message": "The dish has been deleted"}
