from tempfile import TemporaryDirectory
from unittest.mock import Mock, mock_open, patch
import pytest
from django.core.management import call_command
from utils_tests import RETURNED_JSON_EXERCISES


@pytest.mark.django_db
def test_process_exercise_json(Force, Level, Category, Equipment, Mechanic):
    with TemporaryDirectory():
        mock_file = mock_open()
        with patch("api.management.commands.process_exercise_json.open", mock_file):
            mock_json_load = Mock(side_effect=[RETURNED_JSON_EXERCISES])
            with patch(
                "api.management.commands.process_exercise_json.json.load",
                mock_json_load,
            ):
                call_command("process_exercise_json")

        assert mock_file.call_args[0][0] == "./api/fixtures/exercises.json"
