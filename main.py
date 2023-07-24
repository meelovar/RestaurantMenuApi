from fastapi import (
    APIRouter,
    FastAPI,
)

from routers import (
    dishes,
    menus,
    submenus,
)

app = FastAPI()
api_router = APIRouter(prefix="/api/v1")

api_router.include_router(menus.router)
api_router.include_router(submenus.router)
api_router.include_router(dishes.router)
app.include_router(api_router)
