def test_get_level_list(api_client_user, Level):
    resp = api_client_user.get("/levels/")

    assert resp.status_code == 200
    assert len(resp.json()["results"]) == 3


def test_get_equipment_list(api_client_user, Equipment):
    resp = api_client_user.get("/equipments/")

    assert resp.status_code == 200
    assert len(resp.json()["results"]) == 6


def test_get_category_list(api_client_user, Category):
    resp = api_client_user.get("/categories/")

    assert resp.status_code == 200
    assert len(resp.json()["results"]) == 7


def test_get_mechanic_list(api_client_user, Mechanic):
    resp = api_client_user.get("/mechanics/")

    assert resp.status_code == 200
    assert len(resp.json()["results"]) == 2


def test_get_muscles_list(api_client_user, Muscle):
    resp = api_client_user.get("/muscles/")

    assert resp.status_code == 200
    assert len(resp.json()["results"]) == 10


def test_get_forces_list(api_client_user, Force):
    resp = api_client_user.get("/forces/")

    assert resp.status_code == 200
    assert len(resp.json()["results"]) == 3
