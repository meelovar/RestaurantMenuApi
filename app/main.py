from fastapi import APIRouter, FastAPI

from app.routers import dishes, menus, catalog, submenus

app = FastAPI()
api_router = APIRouter(prefix='/api/v1')

api_router.include_router(menus.router)
api_router.include_router(submenus.router)
api_router.include_router(dishes.router)
api_router.include_router(catalog.router)
app.include_router(api_router)
