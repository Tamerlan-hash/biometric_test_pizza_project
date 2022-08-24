from main import test_client


def test_show_restaurants():
    response = test_client.get("/restaurants")
    assert response.status_code == 200
