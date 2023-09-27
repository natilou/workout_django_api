import pytest


@pytest.mark.django_db
class TestWorkoutSessions:
    def test_user_can_get_workout_session_from_workout(
        self,
        api_client_user,
        client_user,
        Workout,
        ExerciseLog,
        Exercise,
        WorkoutSession,
        WorkoutExercise,
        MusclePerExercise,
    ):
        workout = Workout.objects.get(id=1)
        workout_session = WorkoutSession.objects.create(
            workout=workout,
            start_datetime="2023-01-01 08:00:00",
            end_datetime="2023-01-01 08:30:00",
            location="Gym",
        )

        for exercise in Exercise.objects.filter(workouts_exercises__workout=workout):
            ExerciseLog.objects.create(
                exercise=exercise,
                sets_made=4,
                reps_per_set_made=[8, 8, 10, 10],
                weight_used=[12.0, 12.0, 16.0, 16.0],
                workout_session=workout_session,
            )

        resp = api_client_user.get("/workout_sessions/")
        assert resp.status_code == 200
        data = resp.json()["results"][0]
        assert data["user"]["username"] == client_user.username
        assert data["start_datetime"] == "2023-01-01T08:00:00Z"
        assert data["end_datetime"] == "2023-01-01T08:30:00Z"
        assert data["duration"] == 30.0
        assert data["location"] == "Gym"
        assert data["workout"]["id"] == 1
        assert data["workout"]["exercises"][0]["exercise_logs"] == {
            "sets_made": 4,
            "reps_per_set_made": [8, 8, 10, 10],
            "weight_used": ["12.00", "12.00", "16.00", "16.00"],
        }
        assert data["workout"]["exercises"][1]["exercise_logs"] == {
            "sets_made": 4,
            "reps_per_set_made": [8, 8, 10, 10],
            "weight_used": ["12.00", "12.00", "16.00", "16.00"],
        }

    def test_user_can_get_workout_session_from_exercise(
        self,
        api_client_user,
        client_user,
        ExerciseLog,
        Exercise,
        WorkoutSession,
        WorkoutExercise,
        MusclePerExercise,
    ):
        workout_session = WorkoutSession.objects.create(
            user=client_user,
            start_datetime="2023-01-01 08:00:00",
            end_datetime="2023-01-01 08:30:00",
            location="Home",
        )

        ExerciseLog.objects.create(
            exercise=Exercise.objects.get(id=1),
            sets_made=5,
            reps_per_set_made=[10, 10, 8, 6, 4],
            weight_used=[20.00, 20.00, 30.00, 40.00, 50.00],
            workout_session=workout_session,
        )

        resp = api_client_user.get("/workout_sessions/")
        assert resp.status_code == 200

        data = resp.json()["results"][0]
        assert data["start_datetime"] == "2023-01-01T08:00:00Z"
        assert data["end_datetime"] == "2023-01-01T08:30:00Z"
        assert data["duration"] == 30.0
        assert data["location"] == "Home"
        assert data["exercise_log"]["exercise"]["id"] == 1
        assert data["exercise_log"]["exercise"]["name"] == "Press Sit-Up"
        assert data["exercise_log"]["sets_made"] == 5
        assert data["exercise_log"]["reps_per_set_made"] == [10, 10, 8, 6, 4]
        assert data["exercise_log"]["weight_used"] == ["20.00", "20.00", "30.00", "40.00", "50.00"]

    def test_user_has_not_workout_session(self, api_client_user):
        resp = api_client_user.get("/workout_sessions/")
        assert resp.status_code == 200
        assert resp.json()["results"] == []

    def test_user_can_get_all_three_previous_workout_sessions_(
        self,
        api_client_user,
        client_user,
        Workout,
        ExerciseLog,
        Exercise,
        WorkoutSession,
        WorkoutExercise,
        MusclePerExercise,
    ):
        workout_1 = Workout.objects.get(id=1)
        workout_2 = Workout.objects.get(id=2)
        workout_session_1 = WorkoutSession.objects.create(
            workout=workout_1,
            start_datetime="2022-10-01 08:00:00",
            end_datetime="2022-10-01 08:30:00",
            location="Gym",
        )
        workout_session_2 = WorkoutSession.objects.create(
            workout=workout_2,
            start_datetime="2022-10-03 08:00:00",
            end_datetime="2022-10-03 08:30:00",
            location="Home",
        )
        workout_session_3 = WorkoutSession.objects.create(
            user=client_user,
            start_datetime="2022-10-05 08:00:00",
            end_datetime="2022-10-05 08:30:00",
            location="Outdoor",
        )

        for exercise in Exercise.objects.filter(workouts_exercises__workout=workout_1):
            ExerciseLog.objects.create(
                exercise=exercise,
                sets_made=4,
                reps_per_set_made=[8, 8, 10, 10],
                weight_used=[12.0, 12.0, 16.0, 16.0],
                workout_session=workout_session_1,
            )

        for exercise in Exercise.objects.filter(workouts_exercises__workout=workout_2):
            ExerciseLog.objects.create(
                exercise=exercise,
                sets_made=4,
                reps_per_set_made=[8, 8, 10, 10],
                weight_used=[12.0, 12.0, 16.0, 16.0],
                workout_session=workout_session_2,
            )

        ExerciseLog.objects.create(
                exercise=Exercise.objects.get(id=1),
                sets_made=4,
                reps_per_set_made=[8, 8, 10, 10],
                weight_used=[12.0, 12.0, 16.0, 16.0],
                workout_session=workout_session_3,
            )

        resp = api_client_user.get("/workout_sessions/")
        assert resp.status_code == 200

        data = resp.json()["results"]
        assert len(data) == 3
