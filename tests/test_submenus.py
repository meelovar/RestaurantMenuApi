import pytest
from httpx import AsyncClient
from starlette import status

from tests.conftest import State


@pytest.mark.asyncio
async def test_submenu_empty(client: AsyncClient, menu_id: str):
    response = await client.get(f'/menus/{menu_id}/submenus')

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []


@pytest.mark.asyncio
async def test_submenu_create(client: AsyncClient, menu_id: str, state: State):
    submenu_data = {
        'title': 'My submenu 1',
        'description': 'My submenu description 1'
    }
    response = await client.post(f'/menus/{menu_id}/submenus', json=submenu_data)
    response_json = response.json()

    state.id = response_json['id']
    state.title = response_json['title']
    state.description = response_json['description']

    assert response.status_code == status.HTTP_201_CREATED
    assert response_json['title'] == submenu_data['title']
    assert response_json['description'] == submenu_data['description']


@pytest.mark.asyncio
async def test_submenu_list(client: AsyncClient, menu_id: str):
    response = await client.get(f'/menus/{menu_id}/submenus')

    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0


@pytest.mark.asyncio
async def test_submenu_get(client: AsyncClient, menu_id: str, state: State):
    response = await client.get(f'/menus/{menu_id}/submenus/{state.id}')

    assert response.status_code == status.HTTP_200_OK
    assert response.json()['id'] == state.id
    assert response.json()['title'] == state.title
    assert response.json()['description'] == state.description


@pytest.mark.asyncio
async def test_submenu_patch(client: AsyncClient, menu_id: str, state: State):
    submenu_data = {
        'title': 'My updated submenu 1',
        'description': 'My updated submenu description 1'
    }
    response = await client.patch(f'/menus/{menu_id}/submenus/{state.id}', json=submenu_data)
    response_json = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert response_json['title'] == submenu_data['title']
    assert response_json['description'] == submenu_data['description']


@pytest.mark.asyncio
async def test_submenu_delete(client: AsyncClient, menu_id: str, state: State):
    response = await client.delete(f'/menus/{menu_id}/submenus/{state.id}')

    assert response.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
async def test_submenu_get_404(client: AsyncClient, menu_id: str, state: State):
    response = await client.delete(f'/menus/{menu_id}/submenus/{state.id}')

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()['detail'] == 'submenu not found'
