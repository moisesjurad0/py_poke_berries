from fastapi.testclient import TestClient

from ...app.main import app

client = TestClient(app)


def test_poke_berries():
    response = client.get("/api/v1/poke-berries/allBerryStats")
    assert response.status_code == 200


def test_histogram():
    response = client.get("/api/v1/poke-berries/histogram")
    assert response.status_code == 200
    # assert response.
