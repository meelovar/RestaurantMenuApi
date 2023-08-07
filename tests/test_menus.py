import pytest
from httpx import AsyncClient
from starlette import status


@pytest.mark.asyncio
async def test_menus_list_empty(client: AsyncClient):
    response = await client.get('/menus')

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []


@pytest.mark.asyncio
async def test_menu_create(client: AsyncClient, state):
    menu_data = {
        'title': 'My menu 1',
        'description': 'My menu description 1'
    }
    response = await client.post('/menus', json=menu_data)
    response_json = response.json()

    state.id = response_json['id']
    state.title = response_json['title']
    state.description = response_json['description']

    assert response.status_code == status.HTTP_201_CREATED
    assert response_json['title'] == menu_data['title']
    assert response_json['description'] == menu_data['description']


@pytest.mark.asyncio
async def test_menu_list(client: AsyncClient):
    response = await client.get('/menus')

    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0


@pytest.mark.asyncio
async def test_menu_get(client: AsyncClient, state):
    response = await client.get(f'/menus/{state.id}')

    assert response.status_code == status.HTTP_200_OK
    assert response.json()['id'] == state.id
    assert response.json()['title'] == state.title
    assert response.json()['description'] == state.description


@pytest.mark.asyncio
async def test_menu_patch(client: AsyncClient, state):
    new_menu_data = {
        'title': 'My updated menu 1',
        'description': 'My updated menu description 1'
    }
    response = await client.patch(f'/menus/{state.id}', json=new_menu_data)
    response_json = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert response_json['title'] == new_menu_data['title']
    assert response_json['description'] == new_menu_data['description']


@pytest.mark.asyncio
async def test_menu_delete(client: AsyncClient, state):
    response = await client.delete(f'/menus/{state.id}')

    assert response.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
async def test_menu_get_404(client: AsyncClient, state):
    response = await client.delete(f'/menus/{state.id}')

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()['detail'] == 'menu not found'
