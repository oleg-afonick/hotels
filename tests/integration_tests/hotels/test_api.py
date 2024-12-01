import json


async def test_get_hotels(ac):
    response = await ac.get(
        "/hotels",
        params=dict(date_from="2024-12-15", date_to="2024-12-30")
    )
    assert response.status_code == 200
    print("***********")
    print(f"{response.json()=}")
    print("***********")