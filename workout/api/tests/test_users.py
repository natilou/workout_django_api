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


def test_admin_user_can_create_level(api_client_admin, Level):
    resp = api_client_admin.post("/levels/", {"name": "new level"})
    level_created = Level.objects.get(name="new level")

    assert resp.status_code == 201
    assert level_created is not None


def test_admin_user_can_create_equipment(api_client_admin, Equipment):
    resp = api_client_admin.post("/equipments/", {"name": "ball"})
    equipment_created = Equipment.objects.get(name="ball")

    assert resp.status_code == 201
    assert equipment_created is not None


def test_admin_user_can_create_mechanic(api_client_admin, Mechanic):
    resp = api_client_admin.post("/mechanics/", {"name": "new mechanic"})
    mechanic_created = Mechanic.objects.get(name="new mechanic")

    assert resp.status_code == 201
    assert mechanic_created is not None


def test_admin_user_can_create_muscle(api_client_admin, Muscle):
    resp = api_client_admin.post("/muscles/", {"name": "oblique abs"})
    muscle_created = Muscle.objects.get(name="oblique abs")

    assert resp.status_code == 201
    assert muscle_created is not None


def test_admin_user_can_create_force(api_client_admin, Force):
    resp = api_client_admin.post("/forces/", {"name": "super pull"})
    force_created = Force.objects.get(name="super pull")

    assert resp.status_code == 201
    assert force_created is not None


def test_admin_user_can_create_category(api_client_admin, Category):
    resp = api_client_admin.post("/categories/", {"name": "calisthenics"})
    category_created = Category.objects.get(name="calisthenics")

    assert resp.status_code == 201
    assert category_created is not None
