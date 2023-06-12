import pytest


@pytest.mark.django_db
class TestFavoriteWorkout:
    def test_client_user_add_favorite_workout(self, api_client_user, Workout):
        workout = Workout.objects.get(id=1)
        resp = api_client_user.patch(
            f"/workouts/{workout.id}/",
            {
                "is_favorite": True,
            },
        )
        assert resp.status_code == 200

        workout.refresh_from_db()
        assert workout.is_favorite is True

    def test_client_user_cannot_add_favorite_workout(
        self, api_client_other_user, Workout
    ):
        resp = api_client_other_user.patch(
            "/workouts/1/",
            {
                "is_favorite": True,
            },
        )
        assert resp.status_code == 403
        assert resp.json() == {"detail": "Action not allowed"}

    def test_admin_user_cannot_add_favorite_workout(
        self, api_client_admin, Workout
    ):
        resp = api_client_admin.patch(
            "/workouts/1/",
            {
                "is_favorite": True,
            },
        )
        assert resp.status_code == 403
        assert resp.json() == {"detail": "Action not allowed"}
