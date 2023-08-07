import asyncio
import dataclasses

import pytest
import pytest_asyncio
import redis.asyncio as redis
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    create_async_engine,
)

from app.config import (
    DB_HOST_TEST,
    DB_NAME_TEST,
    DB_PASS_TEST,
    DB_PORT_TEST,
    DB_USER_TEST,
    REDIS_HOST_TEST,
)
from app.database import (
    get_async_session,
    get_redis_session,
)
from app.main import app
from app.models import BaseModel

DB_TEST_URL_ASYNC = f'postgresql+asyncpg://{DB_USER_TEST}:{DB_PASS_TEST}@{DB_HOST_TEST}:{DB_PORT_TEST}/{DB_NAME_TEST}'
REDIS_URL = f'redis://{REDIS_HOST_TEST}'

async_engine = create_async_engine(DB_TEST_URL_ASYNC)


@dataclasses.dataclass
class State:
    id: str | None = None
    title: str | None = None
    description: str | None = None


@dataclasses.dataclass
class DishState(State):
    price: str | None = None


async def override_get_async_session():
    async_session = async_sessionmaker(async_engine)

    async with async_session() as session:
        yield session


async def override_get_redis_session():
    async with redis.from_url(REDIS_URL) as session:
        yield session


@pytest_asyncio.fixture(scope='session')
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()

    yield loop

    loop.close()


@pytest_asyncio.fixture(autouse=True, scope='session')
async def prepare_database():
    async with async_engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.create_all)

    yield

    async with async_engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.drop_all)


@pytest_asyncio.fixture(scope='session', name='client')
async def get_client():
    app.dependency_overrides[get_async_session] = override_get_async_session
    app.dependency_overrides[get_redis_session] = override_get_redis_session

    async with AsyncClient(app=app, base_url='http://localhost/api/v1') as c:
        yield c


@pytest.fixture(scope='module', name='state')
def get_state():
    yield State()


@pytest.fixture(scope='module', name='dish_state')
def get_dish_state():
    yield DishState()


@pytest_asyncio.fixture(scope='module', name='menu_id')
async def get_menu_id(client: AsyncClient):
    menu_data = {'title': 'Menu 1', 'description': 'Menu description 1'}
    response = await client.post('/menus', json=menu_data)
    menu_id = response.json()['id']

    yield menu_id

    await client.delete(f'/menus/{menu_id}')


@pytest_asyncio.fixture(scope='module', name='menu_and_submenu_ids')
async def get_menu_and_submenu_ids(client: AsyncClient, menu_id: str):
    submenu_data = {'title': 'Submenu 1', 'description': 'Submenu 1 description'}
    response = await client.post(f'/menus/{menu_id}/submenus', json=submenu_data)
    result = {
        'menu_id': menu_id,
        'submenu_id': response.json()['id']
    }

    yield result


@pytest_asyncio.fixture(scope='module', name='dishes_counts_fixture')
async def get_dishes_counts_fixture(client: AsyncClient, menu_and_submenu_ids: dict[str, str]):
    dish_data1 = {
        'title': 'My dish 1',
        'description': 'My dish description 1',
        'price': '12.50'
    }
    dish_data2 = {
        'title': 'My dish 2',
        'description': 'My dish description 2',
        'price': '13.50'
    }
    menu_id = menu_and_submenu_ids['menu_id']
    submenu_id = menu_and_submenu_ids['submenu_id']

    await client.post(f'/menus/{menu_id}/submenus/{submenu_id}/dishes', json=dish_data1)
    await client.post(f'/menus/{menu_id}/submenus/{submenu_id}/dishes', json=dish_data2)

    yield menu_and_submenu_ids
