"""
Unit tests for knowlift.domain.interval_count_game.

Classes
-------
    TestIntervalOperations: Tests interval operations and result logic.
"""

# Standard library
import unittest
from unittest import mock

# Project specific
from knowlift.domain import interval_count_game


class TestIntervalOperations(unittest.TestCase):
    """
    Unit tests for interval operations and result logic.

    Methods
    -------
    test_calculate_statistics
        Test correct/incorrect stats calculation.
    test_change_game_level
        Test game difficulty level changes.
    test_fetch_game_level
        Test fetching game level by index/input.
    test_generate_result_correct_values
        Test result generation for valid intervals.
    test_generate_result_incorrect_values
        Test result generation for invalid intervals.
    test_prettify_number
        Test number formatting.
    """

    def setUp(self):
        self.metadata = (
            "cpu_internal",
            "cpu_representation",
            "answer_representation",
            "outcome",
            "left_glyph",
            "right_glyph",
            "answer",
            "game_level",
            "start_representation",
            "stop_representation",
            "start_internal",
            "stop_internal",
        )

    def test_calculate_statistics(self):
        test_cases = [
            ((3, 20), (13.04, 86.96)),
            ((3.0, 15), (16.67, 83.33)),
            ((19, 20), (48.72, 51.28)),
            ((15.0, 20), (42.86, 57.14)),
            ((20.0, 20), (50.0, 50.0)),
        ]

        for (incorrect, total), expected in test_cases:
            with self.subTest(incorrect=incorrect, total=total):
                self.assertEqual(
                    interval_count_game.calculate_statistics(incorrect, total),
                    expected,
                )

    @mock.patch("knowlift.domain.interval_count_game.logger")
    def test_change_game_level(self, mock_logger):
        increase_level_answers = [
            6,
            4,
            0,
        ]  # correct_answers, incorrect_answers, current_game_level
        decrease_level_answers = [4, 6, 11]

        for evaluation in range(24):
            if evaluation < 11:
                result_increased = interval_count_game.change_game_level(
                    *increase_level_answers
                )
                self.assertEqual(
                    result_increased, increase_level_answers[2] + 1
                )
                increase_level_answers[2] = result_increased
                mock_logger.info.assert_not_called()
            elif evaluation == 11:
                result_increased = interval_count_game.change_game_level(
                    *increase_level_answers
                )
                self.assertEqual(
                    result_increased, increase_level_answers[2]
                )  # don't go above 10
                mock_logger.info.assert_called_with("Maximum level reached")
                mock_logger.reset_mock()
            elif evaluation < 23:
                result_descreased = interval_count_game.change_game_level(
                    *decrease_level_answers
                )
                self.assertEqual(
                    result_descreased, decrease_level_answers[2] - 1
                )
                decrease_level_answers[2] = result_descreased
                mock_logger.info.assert_not_called()
            else:
                result_descreased = interval_count_game.change_game_level(
                    *decrease_level_answers
                )
                self.assertEqual(
                    result_descreased, decrease_level_answers[2]
                )  # don't go below 0
                mock_logger.info.assert_called_with("Minimum level reached")
                mock_logger.reset_mock()

    @mock.patch("knowlift.domain.interval_count_game.logger")
    def test_fetch_game_level(self, mock_logger):
        valid_inputs = [("0", 0), ("7", 7)]

        # Test invalid inputs that should trigger ValueError logging
        value_error_inputs = ["bogus", "3.14"]
        for invalid_input in value_error_inputs:
            with self.subTest(input=invalid_input):
                result = interval_count_game.fetch_game_level(invalid_input)
                self.assertIsNone(result)
                mock_logger.error.assert_called()
                mock_logger.reset_mock()

        # Test out-of-range inputs that should trigger index error logging
        range_error_inputs = ["15", "12", "-1"]
        for invalid_input in range_error_inputs:
            with self.subTest(input=invalid_input):
                result = interval_count_game.fetch_game_level(invalid_input)
                self.assertIsNone(result)
                mock_logger.error.assert_called_with(
                    "Unable to fetch the game level with index: %s",
                    int(invalid_input),
                )
                mock_logger.reset_mock()

        for input_str, expected_index in valid_inputs:
            with self.subTest(input=input_str):
                result = interval_count_game.fetch_game_level(input_str)
                self.assertEqual(
                    result, interval_count_game.GAME_LEVELS[expected_index]
                )
                mock_logger.error.assert_not_called()

    @mock.patch("knowlift.domain.interval_count_game.logger")
    def test_generate_result_correct_values(self, mock_logger):
        correct_intervals = [
            {
                "left_glyph": "(",
                "right_glyph": ")",
                "start_internal": 7,
                "stop_internal": 41,
                "start_representation": "7",
                "stop_representation": "41",
                "answer": 33,
                "game_level": 0,
                "expected_cpu": 33,
                "expected_repr": "33",
            },
            {
                "left_glyph": "[",
                "right_glyph": ")",
                "start_internal": 7,
                "stop_internal": 41,
                "start_representation": "7",
                "stop_representation": "41",
                "answer": 34,
                "game_level": 0,
                "expected_cpu": 34,
                "expected_repr": "34",
            },
            {
                "left_glyph": "[",
                "right_glyph": "]",
                "start_internal": 7,
                "stop_internal": 41,
                "start_representation": "7",
                "stop_representation": "41",
                "answer": 35,
                "game_level": 0,
                "expected_cpu": 35,
                "expected_repr": "35",
            },
            {
                "left_glyph": "(",
                "right_glyph": ")",
                "start_internal": 200000000,
                "game_level": 11,
                "stop_internal": 350000001,
                "start_representation": "200 000 000",
                "answer": 150000000,
                "stop_representation": "350 000 001",
                "expected_cpu": 150000000,
                "expected_repr": "150 000 000",
            },
        ]

        invalid_glyphs = {
            "left_glyph": ("|", "{", "/", "]", ")"),
            "right_glyph": ("|", "}", "/", "[", "("),
        }

        # Test invalid glyph values (should trigger logger.error)
        for glyph_type, invalid_values in invalid_glyphs.items():
            for glyph in invalid_values:
                with self.subTest(glyph_type=glyph_type, glyph=glyph):
                    sample_interval = correct_intervals[0].copy()
                    sample_interval[glyph_type] = glyph
                    result = interval_count_game.generate_result(
                        sample_interval
                    )
                    self.assertIsNone(result)
                    mock_logger.error.assert_called_with(
                        "unexpected glyph %s", glyph
                    )
                    mock_logger.reset_mock()

        # Test correct intervals (should not trigger any logging)
        for i, interval_data in enumerate(correct_intervals):
            expected_cpu = interval_data.pop("expected_cpu")
            expected_repr = interval_data.pop("expected_repr")

            with self.subTest(interval=i):
                result = interval_count_game.generate_result(interval_data)
                self.assertIsNotNone(result)
                self.assertEqual(
                    result["answer_representation"], expected_repr
                )
                self.assertEqual(result["cpu_representation"], expected_repr)
                self.assertEqual(result["cpu_internal"], expected_cpu)
                self.assertTrue(result["outcome"])
                self.assertTrue(
                    all(element in result for element in self.metadata)
                )
                mock_logger.error.assert_not_called()
                mock_logger.reset_mock()

    @mock.patch("knowlift.domain.interval_count_game.logger")
    def test_generate_result_incorrect_values(self, mock_logger):
        base_interval = {
            "left_glyph": "(",
            "right_glyph": ")",
            "start_internal": 7,
            "stop_internal": 41,
            "start_representation": "7",
            "stop_representation": "41",
            "answer": 38,
            "game_level": 0,
        }

        invalid_intervals = [
            {
                "left_glyph": "[",
                "right_glyph": "]",
                "start_internal": 41,
                "stop_internal": 7,
                "start_representation": "7",
                "stop_representation": "41",
                "answer": 35,
                "game_level": 0,
            },
            {
                "left_glyph": "[",
                "right_glyph": "]",
                "start_internal": 41,
                "stop_internal": 7,
                "start_representation": "41",
                "stop_representation": "7",
                "answer": 35,
                "game_level": 0,
            },
        ]

        # Test missing keys (should trigger logger.error for missing form data)
        for key in base_interval:
            with self.subTest(missing_key=key):
                incomplete_interval = base_interval.copy()
                incomplete_interval.pop(key)
                result = interval_count_game.generate_result(
                    incomplete_interval
                )
                self.assertIsNone(result)
                mock_logger.error.assert_called_with(
                    "%s not found in form data.", key
                )
                mock_logger.reset_mock()

        # Test wrong answer case (should not trigger any error logging)
        result = interval_count_game.generate_result(base_interval)
        self.assertIsNotNone(result)
        self.assertEqual(result["answer_representation"], "38")
        self.assertEqual(result["cpu_representation"], "33")
        self.assertEqual(result["cpu_internal"], 33)
        self.assertFalse(result["outcome"])
        self.assertTrue(all(element in result for element in self.metadata))
        mock_logger.error.assert_not_called()
        mock_logger.reset_mock()

        # Test invalid intervals (should trigger inconsistency error logging)
        for i, interval in enumerate(invalid_intervals):
            with self.subTest(invalid_interval=i):
                result = interval_count_game.generate_result(interval)
                self.assertIsNone(result)
                # Should log inconsistency among numbers
                mock_logger.error.assert_called()
                mock_logger.reset_mock()

    def test_prettify_number(self):
        test_cases = [
            (100, "100"),
            (-100, "-100"),
            (1000, "1 000"),
            (-1000, "-1 000"),
            (10000, "10 000"),
            (-10000, "-10 000"),
            (100000, "100 000"),
            (-100000, "-100 000"),
            (1000000, "1 000 000"),
            (-1000000, "-1 000 000"),
        ]

        for number, expected in test_cases:
            with self.subTest(number=number):
                self.assertEqual(
                    interval_count_game.prettify_number(number), expected
                )
