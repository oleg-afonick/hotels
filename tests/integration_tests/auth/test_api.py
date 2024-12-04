async def test_auth(ac):
    user_data = {"email": "user1@test.ru", "password": "password1"}
    login_user = await ac.post("/auth/register", json=user_data)
    assert login_user.json()["status"] == "OK"

    await ac.post("/auth/login", json=user_data)
    access_token = ac.cookies["access_token"]
    assert access_token

    current_user = await ac.get("/auth/current_user")
    assert current_user.json()["email"] == user_data["email"]

    logout_user = await ac.get("/auth/logout")
    assert logout_user.json()["status"] == "OK"
    get_cookies = ac.cookies
    assert not get_cookies

    current_user = await ac.get("/auth/current_user")
    user_data = current_user.json()
    assert user_data["detail"] == "Пользователь не аутентифицирован"
