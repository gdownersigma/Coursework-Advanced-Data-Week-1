"""Script to test the functions in load.py"""

from unittest.mock import MagicMock
from load import insert_kiosk_data


class TestInsertKioskData:
    """Tests for insert_kiosk_data function."""

    def test_inserts_review_when_val_is_rating(self):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_logger = MagicMock()

        data = {"at": "2026-01-05T10:00:00", "site": 2, "val": 3}
        insert_kiosk_data(mock_conn, data, mock_logger)

        # Check it called INSERT INTO review
        call_args = mock_cursor.execute.call_args[0][0]
        assert "INSERT INTO review" in call_args
        mock_conn.commit.assert_called_once()

    def test_inserts_incident_when_val_is_minus_one(self):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_logger = MagicMock()

        data = {"at": "2026-01-05T10:00:00", "site": 1, "val": -1, "type": 0}
        insert_kiosk_data(mock_conn, data, mock_logger)

        # Check it called INSERT INTO incident
        call_args = mock_cursor.execute.call_args[0][0]
        assert "INSERT INTO incident" in call_args
        mock_conn.commit.assert_called_once()
