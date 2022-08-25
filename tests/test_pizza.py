# from fastapi.testclient import TestClient
#
# from main import app
#
#
# def test_show_restaurant_pizzas():
#     client = TestClient(app)
#     response = client.get("/restaurants", params={"page": 1, "size": 50})
#     assert response.status_code == 200
#     restaurants = response.json()['data']
#     if len(restaurants):
#         response = client.get(
#             f"/restaurants/{restaurants[-1]['id']}/pizzas",
#             params={"page": 1, "size": 50}
#         )
#         data = response.json()['data']
#         assert response.status_code == 200
#         if not len(data):
#             assert data == []
#         else:
#             pizza = data[-1]
#             assert type(pizza['id']) == int
#             assert type(pizza['name']) == str
#             assert type(pizza['thickness']) == str
#             assert type(pizza['secret_ingredient']) == str | None
