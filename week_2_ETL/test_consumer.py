"""Script to test the validation and cleaning functions in consumer.py"""

from consumer import validate_message, clean_message
from datetime import datetime, time


class TestValidateMessage:
    """All tests for validate_message function."""

    def test_valid_review(self):
        data = {"val": 3, "site": "2", "at": "2024-06-15T10:30:00"}
        assert validate_message(data) == True

    def test_valid_incident(self):
        data = {"val": -1, "site": "2", "at": "2024-06-15T10:30:00", "type": 0}
        assert validate_message(data) == True

    def test_missing_val(self):
        data = {"at": "2026-01-05T10:00:00+00:00", "site": "2"}
        assert validate_message(data) == False

    def test_invalid_val_string(self):
        data = {"at": "2026-01-05T10:00:00+00:00", "site": "2", "val": "ERR"}
        assert validate_message(data) == False

    def test_invalid_val_out_of_range(self):
        data = {"at": "2026-01-05T10:00:00+00:00", "site": "2", "val": 5}
        assert validate_message(data) == False

    def test_invalid_site(self):
        data = {"at": "2026-01-05T10:00:00+00:00", "site": "9", "val": 3}
        assert validate_message(data) == False

    def test_outside_opening_hours_too_early(self):
        data = {"at": "2026-01-05T08:00:00+00:00", "site": "2", "val": 3}
        assert validate_message(data) == False

    def test_outside_opening_hours_too_late(self):
        data = {"at": "2026-01-05T19:00:00+00:00", "site": "2", "val": 3}
        assert validate_message(data) == False

    def test_invalid_type_value(self):
        data = {"at": "2026-01-05T10:00:00+00:00",
                "site": "1", "val": -1, "type": 5}
        assert validate_message(data) == False


class TestCleanMessage:
    """All tests for clean_message function."""

    def test_converts_site_to_int(self):
        data = {"at": "2026-01-05T10:00:00", "site": "2", "val": 3}
        result = clean_message(data)
        assert result["site"] == 2
        assert isinstance(result["site"], int)

    def test_preserves_val(self):
        data = {"at": "2026-01-05T10:00:00", "site": "2", "val": 3}
        result = clean_message(data)
        assert result["val"] == 3

    def test_includes_type_when_present(self):
        data = {"at": "2026-01-05T10:00:00", "site": "1", "val": -1, "type": 0}
        result = clean_message(data)
        assert result["type"] == 0

    def test_excludes_type_when_absent(self):
        data = {"at": "2026-01-05T10:00:00", "site": "2", "val": 3}
        result = clean_message(data)
        assert "type" not in result
