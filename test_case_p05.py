# Harsha Karapureddy
# CS 3354
# Group 6
# File Description: Tests reccomendation file. IMPORTANT: THERE IS NO TEST CASE FOR SUCCESS AS RETURN VALUE ARE UNPREDICTABLE

import unittest
from unittest.mock import patch
from reccomendation_system_t import recommend_games_for_user


class test_invalid_userid(unittest.TestCase):

    # TC1
    @patch("builtins.print")
    def test_invalid_userid(self, mock_print):
        recommend_games_for_user("abc123")
        mock_print.assert_called_with("Error: Invalid userID")

    # TC2
    @patch("builtins.print")
    def test_empty_userid(self, mock_print):
        recommend_games_for_user("")
        mock_print.assert_called_with("Error: Invalid userID")


if __name__ == "__main__":
    unittest.main()
