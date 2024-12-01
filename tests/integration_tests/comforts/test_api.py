import json


async def test_add_comforts(ac):
    with open("tests/mocks/mock_comforts.json", encoding="utf-8") as file:
        comforts_data = json.load(file)
    for comfort in comforts_data:
        response = await ac.post("/comforts", json=comfort)
        assert response.status_code == 200


async def test_get_comforts(ac):
    with open("tests/mocks/mock_comforts.json", encoding="utf-8") as file:
        comforts_data = json.load(file)

    response = await ac.get("/comforts")
    assert response.status_code == 200

    comforts_response = response.json()
    assert len(comforts_data) == len(comforts_response)

    for comfort_data, comfort_response in zip(comforts_data, comforts_response):
        assert comfort_data.get("title") == comfort_response.get("title")