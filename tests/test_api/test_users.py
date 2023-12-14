STATUS_CREATED = 201

async def test_user_registration(client):
    response = await client.post(
        "/auth/register",
        json={
            "username": "test1",
            "password": "test1234",
        },
    )

    assert response.status_code == STATUS_CREATED
    assert response.json()["username"] == "test1"
    assert response.json()["role"] == "client"
