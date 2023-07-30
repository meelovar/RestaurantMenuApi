import pytest
from httpx import (
    AsyncClient,
)
from starlette import status

from tests.conftest import DishState


@pytest.mark.asyncio
async def test_dishes_list_empty(client: AsyncClient, menu_and_submenu_ids: dict[str, str]):
    menu_id = menu_and_submenu_ids["menu_id"]
    submenu_id = menu_and_submenu_ids["submenu_id"]
    response = await client.get(f"/menus/{menu_id}/submenus/{submenu_id}/dishes")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []


@pytest.mark.asyncio
async def test_dishes_create(client: AsyncClient, menu_and_submenu_ids: dict[str, str], dish_state: DishState):
    menu_id = menu_and_submenu_ids["menu_id"]
    submenu_id = menu_and_submenu_ids["submenu_id"]
    dish_data = {
        "title": "My dish 1",
        "description": "My dish description 1",
        "price": "12.50"
    }
    response = await client.post(f"/menus/{menu_id}/submenus/{submenu_id}/dishes", json=dish_data)
    response_json = response.json()

    dish_state.id = response_json["id"]
    dish_state.title = response_json["title"]
    dish_state.description = response_json["description"]
    dish_state.price = response_json["price"]

    assert response.status_code == status.HTTP_201_CREATED
    assert response_json["title"] == dish_data["title"]
    assert response_json["description"] == dish_data["description"]
    assert response_json["price"] == dish_data["price"]


@pytest.mark.asyncio
async def test_dishes_list(client: AsyncClient, menu_and_submenu_ids: dict[str, str]):
    menu_id = menu_and_submenu_ids["menu_id"]
    submenu_id = menu_and_submenu_ids["submenu_id"]
    response = await client.get(f"/menus/{menu_id}/submenus/{submenu_id}/dishes")

    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0


@pytest.mark.asyncio
async def test_dishes_get(client: AsyncClient, menu_and_submenu_ids: dict[str, str], dish_state: DishState):
    menu_id = menu_and_submenu_ids["menu_id"]
    submenu_id = menu_and_submenu_ids["submenu_id"]
    response = await client.get(f"/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_state.id}")

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["id"] == dish_state.id
    assert response.json()["title"] == dish_state.title
    assert response.json()["description"] == dish_state.description
    assert response.json()["price"] == dish_state.price


@pytest.mark.asyncio
async def test_dishes_patch(client: AsyncClient, menu_and_submenu_ids: dict[str, str], dish_state: DishState):
    dish_data = {
        "title": "My updated dish 1",
        "description": "My updated dish description 1",
        "price": "14.50"
    }
    menu_id = menu_and_submenu_ids["menu_id"]
    submenu_id = menu_and_submenu_ids["submenu_id"]
    response = await client.patch(f"/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_state.id}", json=dish_data)
    response_json = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert response_json["title"] == dish_data["title"]
    assert response_json["description"] == dish_data["description"]
    assert response_json["price"] == dish_data["price"]


@pytest.mark.asyncio
async def test_dishes_delete(client: AsyncClient, menu_and_submenu_ids: dict[str, str], dish_state: DishState):
    menu_id = menu_and_submenu_ids["menu_id"]
    submenu_id = menu_and_submenu_ids["submenu_id"]
    response = await client.delete(f"/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_state.id}")

    assert response.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
async def test_dishes_get_404(client: AsyncClient, menu_and_submenu_ids: dict[str, str], dish_state: DishState):
    menu_id = menu_and_submenu_ids["menu_id"]
    submenu_id = menu_and_submenu_ids["submenu_id"]
    response = await client.get(f"/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_state.id}")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "dish not found"
