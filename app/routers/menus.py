from uuid import UUID

from fastapi import APIRouter, Depends
from starlette import status

from app.dependencies import valid_menu
from app.models import Menu
from app.schemas import MenuSchemaIn, MenuSchemaOut
from app.services.menus import MenuService

router = APIRouter(prefix='/menus', tags=['menus'])


@router.get('', response_model=list[MenuSchemaOut])
async def get_list(menu_svc: MenuService = Depends()):
    result = await menu_svc.get_list()

    return result


@router.get('/{menu_id}', response_model=MenuSchemaOut)
async def get(menu: Menu = Depends(valid_menu)):
    return menu


@router.post('', response_model=MenuSchemaOut, status_code=status.HTTP_201_CREATED)
async def create(menu_data: MenuSchemaIn, menu_svc: MenuService = Depends()):
    return await menu_svc.create(menu_data)


@router.patch('/{menu_id}', response_model=MenuSchemaOut)
async def update(menu_id: UUID, menu_data: MenuSchemaIn, menu_svc: MenuService = Depends()):
    return await menu_svc.update(menu_id, menu_data)


@router.delete('/{menu_id}')
async def delete(menu_id: UUID, menu_svc: MenuService = Depends()):
    await menu_svc.delete(menu_id)

    return {'status': True, 'message': 'The submenu has been deleted'}
