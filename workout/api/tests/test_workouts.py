from freezegun import freeze_time


@freeze_time("2023-01-01")
def test_client_user_create_workout_routine_by_level_equipment_and_category(
    api_client_user, Exercise
):
    resp = api_client_user.post(
        "/workout/",
        {
            "level": "expert",
            "equipment": "barbell",
            "category": "strength",
            "mechanic": "compound",
        },
    )
    assert resp.status_code == 201
    assert resp.json()["created"] == "2023-01-01"
    assert resp.json()["total_sets"] == {"total_sets__max": 5}
    assert len(resp.json()["reps_per_exercise"]) == 3
    assert len(resp.json()["exercises"]) == 3


@freeze_time("2023-01-01")
def test_client_user_can_create_workout_routine_by_muscle_and_force(
    api_client_user, Exercise, MusclePerExercise
):
    resp = api_client_user.post(
        "/workout/",
        {
            "muscles": ["abs", "shoulders"],
            "force": "pull",
        },
    )
    assert resp.status_code == 201
    assert resp.json()["created"] == "2023-01-01"
    assert resp.json()["total_sets"] == {"total_sets__max": 5}
    assert len(resp.json()["reps_per_exercise"]) == 2
    assert len(resp.json()["exercises"]) == 2
