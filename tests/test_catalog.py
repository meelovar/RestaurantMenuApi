import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_counts_menu_get(client: AsyncClient, dishes_counts_fixture: dict[str, str]):
    response = await client.get('/catalog')
    response_json = response.json()

    assert len(response_json) == 2
    assert len(response_json[0]['submenus']) == 1
    assert len(response.json()[0]['submenus'][0]['dishes']) == 2
