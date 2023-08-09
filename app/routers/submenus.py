from typing import Mapping
from uuid import UUID

from fastapi import APIRouter, Depends
from starlette import status

from app.dependencies import valid_submenu
from app.schemas import SubmenuSchemaIn, SubmenuSchemaOut
from app.services import SubmenuService

router = APIRouter(prefix='/menus/{menu_id}/submenus', tags=['submenus'])


@router.get('', response_model=list[SubmenuSchemaOut])
async def get_list(menu_id: UUID, submenu_svc: SubmenuService = Depends()):
    return await submenu_svc.get_list(menu_id)


@router.get('/{submenu_id}', response_model=SubmenuSchemaOut)
async def get(submenu: Mapping = Depends(valid_submenu)):
    return submenu


@router.post('', response_model=SubmenuSchemaOut, status_code=status.HTTP_201_CREATED)
async def create(menu_id: UUID, submenu_data: SubmenuSchemaIn, submenu_svc: SubmenuService = Depends()):
    return await submenu_svc.create(menu_id, submenu_data)


@router.patch('/{submenu_id}', response_model=SubmenuSchemaOut)
async def update(
        menu_id: UUID,
        submenu_id: UUID,
        submenu_data: SubmenuSchemaIn,
        submenu_svc: SubmenuService = Depends()
):
    return await submenu_svc.update(menu_id, submenu_id, submenu_data)


@router.delete('/{submenu_id}')
async def delete(menu_id: UUID, submenu_id: UUID, submenu_svc: SubmenuService = Depends()):
    await submenu_svc.delete(menu_id, submenu_id)

    return {'status': True, 'message': 'The dish has been deleted'}
