from tempfile import TemporaryDirectory
from unittest.mock import Mock, mock_open, patch

import pytest
from api.read_json import read_json
from utils_tests import RETURNED_JSON_EXERCISES


@pytest.mark.parametrize(
    "field,expected_path",
    [
        ("category", "./fixtures/category.json"),
        ("force", "./fixtures/force.json"),
        ("level", "./fixtures/level.json"),
        ("muscle", "./fixtures/muscle.json"),
    ],
)
def test_read_json(field, expected_path):
    with TemporaryDirectory():
        mock_file = mock_open()
        with patch("api.read_json.open", mock_file):
            mock_json_load = Mock(side_effect=[RETURNED_JSON_EXERCISES])
            with patch("api.read_json.json.load", mock_json_load):
                read_json(field)

        assert mock_file.call_args[0][0] == expected_path
