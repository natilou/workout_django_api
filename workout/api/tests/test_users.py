def test_get_client_user_needs_token(api_client_user):
    resp = api_client_user.get("/users/")
    assert resp.status_code == 403
    assert resp.json() == {
        "detail": "You do not have permission to perform this action."
    }


def test_get_admin_user_can_access_users(api_client_admin):
    resp = api_client_admin.get("/users/")
    assert resp.status_code == 200, resp.json()
