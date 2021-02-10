from fastapi.testclient import TestClient

from backend.main import app

client = TestClient(app)


def test_read_users():
    """
    Test the /users GET endpoint.

    :return:
    """
    response = client.get("/users")
    assert response.status_code == 200
    assert len(response.json()) == 0


def test_add_users():
    """
    Test the /users POST endpoint.
    :return:
    """
    response = client.post("/users", json={"name": "Tina", "surname": "Belcher"})
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_add_multiple_dataset():
    """
    Test that data is stored in the database correctly.

    :return:
    """
    response = client.get("/users")
    assert response.status_code == 200
    assert len(response.json()) == 0

    response = client.post("/users", json={"name": "Tina", "surname": "Belcher"})
    assert response.status_code == 200

    response = client.get("/users")
    assert response.status_code == 200
    assert len(response.json()) == 1

    response = client.post("/users", json={"name": "Louise", "surname": "Belcher"})
    assert response.status_code == 200

    response = client.get("/users")
    assert response.status_code == 200
    assert len(response.json()) == 2
    print(response.json())
