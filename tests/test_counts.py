import pytest
from httpx import AsyncClient
from starlette import status


@pytest.mark.asyncio
async def test_counts_menu_get(client: AsyncClient, dishes_counts_fixture: dict[str, str]) -> None:
    menu_id = dishes_counts_fixture['menu_id']
    response = await client.get(f'/menus/{menu_id}')
    response_json = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert response_json['id'] == menu_id
    assert response_json['submenus_count'] == 1
    assert response_json['dishes_count'] == 2


@pytest.mark.asyncio
async def test_counts_submenu_get(client: AsyncClient, dishes_counts_fixture: dict[str, str]) -> None:
    menu_id = dishes_counts_fixture['menu_id']
    submenu_id = dishes_counts_fixture['submenu_id']
    response = await client.get(f'/menus/{menu_id}/submenus/{submenu_id}')
    response_json = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert response_json['id'] == submenu_id
    assert response_json['dishes_count'] == 2


@pytest.mark.asyncio
async def test_counts_submenu_delete_cascade(client: AsyncClient, dishes_counts_fixture: dict[str, str]) -> None:
    menu_id = dishes_counts_fixture['menu_id']
    submenu_id = dishes_counts_fixture['submenu_id']
    response = await client.delete(f'/menus/{menu_id}/submenus/{submenu_id}')

    assert response.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
async def test_counts_submenus_list_empty(client: AsyncClient, dishes_counts_fixture: dict[str, str]) -> None:
    menu_id = dishes_counts_fixture['menu_id']
    response = await client.get(f'/menus/{menu_id}/submenus')

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []


@pytest.mark.asyncio
async def test_counts_dishes_list_empty(client: AsyncClient, dishes_counts_fixture: dict[str, str]) -> None:
    menu_id = dishes_counts_fixture['menu_id']
    submenu_id = dishes_counts_fixture['submenu_id']
    response = await client.get(f'/menus/{menu_id}/submenus/{submenu_id}/dishes')

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []


@pytest.mark.asyncio
async def test_counts_menu_counts_zero(client: AsyncClient, dishes_counts_fixture: dict[str, str]) -> None:
    menu_id = dishes_counts_fixture['menu_id']
    response = await client.get(f'/menus/{menu_id}')
    response_json = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert response_json['submenus_count'] == 0
    assert response_json['dishes_count'] == 0
