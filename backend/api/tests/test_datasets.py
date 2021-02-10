from fastapi.testclient import TestClient

from backend.main import app

client = TestClient(app)


def test_read_datasets():
    """
    Test the /datasets GET endpoint.

    :return:
    """
    response = client.get("/datasets")
    assert response.status_code == 200
    assert len(response.json()) == 0


def test_add_dataset():
    """
    Test the /datasets POST endpoint.
    :return:
    """
    response = client.post(
        "/datasets", json={"name": "residential", "description": "Residential data."}
    )
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_add_multiple_dataset():
    """
    Test that data is stored in the database correctly.

    :return:
    """
    response = client.get("/datasets")
    assert response.status_code == 200
    assert len(response.json()) == 0

    response = client.post(
        "/datasets", json={"name": "residential", "description": "Residential data."}
    )
    assert response.status_code == 200

    response = client.get("/datasets")
    assert response.status_code == 200
    assert len(response.json()) == 1

    response = client.post(
        "/datasets", json={"name": "commercial", "description": "Commercial data."}
    )
    assert response.status_code == 200

    response = client.get("/datasets")
    assert response.status_code == 200
    assert len(response.json()) == 2
    print(response.json())
