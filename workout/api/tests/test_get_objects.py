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

    resp2 = api_client_user.get("/muscles/?page=2")
    assert resp2.status_code == 200
    assert len(resp2.json()["results"]) == 1


def test_get_forces_list(api_client_user, Force):
    resp = api_client_user.get("/forces/")

    assert resp.status_code == 200
    assert len(resp.json()["results"]) == 3


def test_get_exercises_list(api_client_user, Exercise):
    resp = api_client_user.get("/exercises/")

    assert resp.status_code == 200
    assert len(resp.json()["results"]) == 3


def test_get_filtered_exercises_list(api_client_user, Exercise, MusclePerExercise):
    resp = api_client_user.get(
        "/exercises/?category=&equipment=&force=&level=&mechanic=&muscle=&primary_muscle=abs&secondary_muscle=shoulders"
    )

    assert resp.status_code == 200
    assert len(resp.json()["results"]) == 1
