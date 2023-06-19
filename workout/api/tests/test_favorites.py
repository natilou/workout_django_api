import pytest
from django.core.exceptions import ObjectDoesNotExist


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

    def test_admin_user_cannot_add_favorite_workout(self, api_client_admin, Workout):
        resp = api_client_admin.patch(
            "/workouts/1/",
            {
                "is_favorite": True,
            },
        )
        assert resp.status_code == 403
        assert resp.json() == {"detail": "Action not allowed"}


@pytest.mark.django_db
class TestFavoriteExercise:
    def test_client_user_add_favorite_exercise(
        self, client_user, api_client_user, Exercise, FavoriteExercise
    ):
        exercise = Exercise.objects.get(id=1)
        resp = api_client_user.post(
            f"/exercises/{exercise.id}/favorite/",
        )
        assert resp.status_code == 201
        assert FavoriteExercise.objects.get(user=client_user, exercise=exercise)

    def test_client_user_delete_favorite_exercise(
        self, client_user, api_client_user, Exercise, FavoriteExercise
    ):
        exercise = Exercise.objects.get(id=1)

        api_client_user.post(
            f"/exercises/{exercise.id}/favorite/",
        )

        resp = api_client_user.delete(
            f"/exercises/{exercise.id}/favorite/",
        )

        assert resp.status_code == 201
        with pytest.raises(ObjectDoesNotExist):
            FavoriteExercise.objects.get(user=client_user, exercise=exercise)

    def test_client_user_can_get_favorite_exercises(self, api_client_user, Exercise):
        exercise = Exercise.objects.get(id=1)
        exercise2 = Exercise.objects.get(id=2)

        api_client_user.post(
            f"/exercises/{exercise.id}/favorite/",
        )

        api_client_user.post(
            f"/exercises/{exercise2.id}/favorite/",
        )

        resp = api_client_user.get(
            "/exercises/?category=&equipment=&force=&level=&mechanic=&muscle=&primary_muscle=&secondary_muscle=&favorites=True",  # noqa
        )

        assert resp.status_code == 200
        assert resp.json()["count"] == 2

    def test_client_already_has_favorite(self, api_client_user, Exercise):
        exercise = Exercise.objects.get(id=1)

        api_client_user.post(
            f"/exercises/{exercise.id}/favorite/",
        )

        resp = api_client_user.post(
            f"/exercises/{exercise.id}/favorite/",
        )

        assert resp.status_code == 400

    def test_client_cannot_delete_non_existing_favorite(
        self, api_client_user, Exercise
    ):
        exercise = Exercise.objects.get(id=1)

        resp = api_client_user.delete(
            f"/exercises/{exercise.id}/favorite/",
        )

        assert resp.status_code == 400
