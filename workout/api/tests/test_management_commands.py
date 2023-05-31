from django.core.management import call_command
from tempfile import TemporaryDirectory
from unittest.mock import mock_open, patch


@patch("api.read_json.json.load")
@patch("api.read_json.json.dumps")
def test_process_exercise_json(mock_json_load, mock_json_dumps):
    with TemporaryDirectory():
        with patch("builtins.open", mock_open()) as open_mocked:
            call_command('process_exercise_json')
        assert open_mocked.call_count == 2
        handle = open_mocked()
        handle.write.assert_called_once()
