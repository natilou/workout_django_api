import pytest
from freezegun import freeze_time


@pytest.mark.django_db
@freeze_time("2023-01-01 08:00:00")
class TestExerciseLogs:
    def test_client_user_add_exercise_log(self, api_client_user, Exercise):
        exercise = Exercise.objects.get(id=3)
        resp = api_client_user.post(
            f"/exercises/{exercise.id}/logs/",
            {
                "sets_made": 3,
                "reps_per_set_made": [10, 8, 6],
                "weight_used": [20.00, 30.00, 40.00],
                "location": "Gym",
                "start_datetime": "2023-01-01 08:00:00",
                "end_datetime": "2023-01-01 08:30:00",
            },
        )
        assert resp.status_code == 201
