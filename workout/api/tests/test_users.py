def test_get_client_user_needs_token(api_client_user):
    resp = api_client_user.get("/users/")
    assert resp.status_code == 403
    assert resp.json() == {
        "detail": "You do not have permission to perform this action."
    }


def test_get_admin_user_can_access_users(api_client_admin):
    resp = api_client_admin.get("/users/")
    assert resp.status_code == 200, resp.json()


def test_client_user_cannot_create_level(api_client_user):
    resp = api_client_user.post("/levels/", {"name": "new level"})

    assert resp.status_code == 403
    assert resp.json() == {
        "detail": "You do not have permission to perform this action."
    }


def test_client_user_cannot_create_equipment(api_client_user):
    resp = api_client_user.post("/equipments/", {"name": "ball"})

    assert resp.status_code == 403
    assert resp.json() == {
        "detail": "You do not have permission to perform this action."
    }


def test_admin_user_can_create_level(api_client_admin):
    resp = api_client_admin.post("/levels/", {"name": "new level"})

    assert resp.status_code == 201
    assert resp.json() == {'id': 4, 'name': 'new level'}


def test_admin_user_can_create_equipment(api_client_admin):
    resp = api_client_admin.post("/equipments/", {"name": "ball"})

    assert resp.status_code == 201
    assert resp.json() == {'id': 7, 'name': 'ball'}


def test_admin_user_can_create_mechanic(api_client_admin):
    resp = api_client_admin.post("/mechanics/", {"name": "new mechanic"})

    assert resp.status_code == 201
    assert resp.json() == {'id': 3, 'name': 'new mechanic'}


def test_admin_user_can_create_muscle(api_client_admin):
    resp = api_client_admin.post("/muscles/", {"name": "oblique abs"})

    assert resp.status_code == 201
    assert resp.json() == {'id': 11, 'name': 'oblique abs'}


def test_admin_user_can_create_force(api_client_admin):
    resp = api_client_admin.post("/forces/", {"name": "super pull"})

    assert resp.status_code == 201
    assert resp.json() == {'id': 4, 'name': 'super pull'}


def test_admin_user_can_create_category(api_client_admin):
    resp = api_client_admin.post("/categories/", {"name": "calisthenics"})

    assert resp.status_code == 201
    assert resp.json() == {'id': 8, 'name': 'calisthenics'}
