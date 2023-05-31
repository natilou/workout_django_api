from tempfile import TemporaryDirectory
from unittest.mock import mock_open, patch

import pytest
from api.read_json import read_json


@pytest.mark.parametrize(
    "field",
    [
        ("category"),
        ("force"),
        ("level"),
        ("muscle"),
    ],
)
@patch("api.read_json.json.load")
@patch("api.read_json.json.dumps")
def test_read_json(mock_json_load, mock_json_dumps, field):
    with TemporaryDirectory():
        with patch("builtins.open", mock_open()) as open_mocked:
            read_json(field)
        assert open_mocked.call_count == 2
        handle = open_mocked()
        handle.write.assert_called_once()
