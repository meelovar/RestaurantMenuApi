from fastapi import APIRouter, Depends

from app.schemas import MenuCatalogSchemaOut
from app.services.menus import CatalogService

router = APIRouter(prefix='/catalog', tags=['catalog'])


@router.get('', response_model=list[MenuCatalogSchemaOut])
async def get_catalog(svc: CatalogService = Depends()):
    result = await svc.get_catalog()

    return result
