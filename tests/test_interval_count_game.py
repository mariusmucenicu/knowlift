"""
Unit tests for knowlift.domain.interval_count_game.

Classes
-------
- TestIntervalOperations: Tests interval operations and result logic.
"""

# Standard library
import unittest

# Project specific
from knowlift.domain import interval_count_game


class TestIntervalOperations(unittest.TestCase):
    """
    Unit tests for interval operations and result logic.

    Methods
    -------
    - test_calculate_statistics:
        Test correct/incorrect stats calculation.

    - test_change_game_level:
        Test game difficulty level changes.

    - test_fetch_game_level:
        Test fetching game level by index/input.

    - test_generate_result_correct_values:
        Test result generation for valid intervals.

    - test_generate_result_incorrect_values:
        Test result generation for invalid intervals.

    - test_prettify_number:
        Test number formatting for readability.
    """

    def setUp(self):
        self.metadata = (
            'cpu_internal',
            'cpu_representation',
            'answer_representation',
            'outcome',
            'left_glyph',
            'right_glyph',
            'answer',
            'game_level',
            'start_representation',
            'stop_representation',
            'start_internal',
            'stop_internal',
        )

    def test_calculate_statistics(self):
        self.assertEqual(interval_count_game.calculate_statistics(3, 20), (13.04, 86.96))
        self.assertEqual(interval_count_game.calculate_statistics(3, 20), (13.04, 86.96))
        self.assertEqual(interval_count_game.calculate_statistics(3.0, 15), (16.67, 83.33))
        self.assertEqual(interval_count_game.calculate_statistics(19, 20), (48.72, 51.28))
        self.assertEqual(interval_count_game.calculate_statistics(15.0, 20), (42.86, 57.14))
        self.assertEqual(interval_count_game.calculate_statistics(20.0, 20), (50.0, 50.0))

    def test_change_game_level(self):
        increase_level_answers = [6, 4, 0]  # correct_answers, incorrect_answers, current_game_level
        decrease_level_answers = [4, 6, 11]

        for evaluation in range(24):
            if evaluation < 11:
                result_increased = interval_count_game.change_game_level(*increase_level_answers)
                self.assertEqual(result_increased, increase_level_answers[2] + 1)
                increase_level_answers[2] = result_increased
            elif evaluation == 11:
                result_increased = interval_count_game.change_game_level(*increase_level_answers)
                self.assertEqual(result_increased, increase_level_answers[2])  # don't go above 10
            elif evaluation < 23:
                result_descreased = interval_count_game.change_game_level(*decrease_level_answers)
                self.assertEqual(result_descreased, decrease_level_answers[2] - 1)
                decrease_level_answers[2] = result_descreased
            else:
                result_descreased = interval_count_game.change_game_level(*decrease_level_answers)
                self.assertEqual(result_descreased, decrease_level_answers[2])  # don't go below 0

    def test_fetch_game_level(self):
        self.assertIsNone(interval_count_game.fetch_game_level('bogus'))
        self.assertIsNone(interval_count_game.fetch_game_level('3.14'))
        self.assertIsNone(interval_count_game.fetch_game_level('15'))
        self.assertIsNone(interval_count_game.fetch_game_level('12'))
        self.assertIsNone(interval_count_game.fetch_game_level('-1'))
        self.assertEqual(interval_count_game.fetch_game_level('0'), interval_count_game.GAME_LEVELS[0])
        self.assertEqual(interval_count_game.fetch_game_level('7'), interval_count_game.GAME_LEVELS[7])

    def test_generate_result_correct_values(self):
        interval_correct_1 = {
            'left_glyph': '(', 'right_glyph': ')', 'start_internal': 7, 'stop_internal': 41,
            'start_representation': '7', 'stop_representation': '41', 'answer': 33, 'game_level': 0
        }
        interval_correct_2 = {
            'left_glyph': '[', 'right_glyph': ')', 'start_internal': 7, 'stop_internal': 41,
            'start_representation': '7', 'stop_representation': '41', 'answer': 34, 'game_level': 0
        }
        interval_correct_3 = {
            'left_glyph': '[', 'right_glyph': ']', 'start_internal': 7, 'stop_internal': 41,
            'start_representation': '7', 'stop_representation': '41', 'answer': 35, 'game_level': 0
        }
        interval_correct_4 = {
            'left_glyph': '(', 'right_glyph': ')', 'start_internal': 200000000, 'game_level': 11,
            'stop_internal': 350000001, 'start_representation': '200 000 000', 'answer': 150000000,
            'stop_representation': '350 000 001',
        }
        invalid_glyphs = {
            'left_glyph': ('|', '{', '/', ']', ')'),
            'right_glyph': ('|', '}', '/', '[', '('),
        }

        # test invalid glyph values
        for glyph_internal, glyph_representation in invalid_glyphs.items():
            sample_correct_interval = interval_correct_1.copy()
            for glyph in glyph_representation:
                sample_correct_interval[glyph_internal] = glyph
                self.assertIsNone(interval_count_game.generate_result(sample_correct_interval))

        generated_values_correct = interval_count_game.generate_result(interval_correct_1)
        generated_values_correct_2 = interval_count_game.generate_result(interval_correct_2)
        generated_values_correct_3 = interval_count_game.generate_result(interval_correct_3)
        generated_values_correct_4 = interval_count_game.generate_result(interval_correct_4)
        self.assertEqual(generated_values_correct['answer_representation'], '33')
        self.assertEqual(generated_values_correct['cpu_representation'], '33')
        self.assertEqual(generated_values_correct['cpu_internal'], 33)
        self.assertEqual(generated_values_correct_2['answer_representation'], '34')
        self.assertEqual(generated_values_correct_2['cpu_representation'], '34')
        self.assertEqual(generated_values_correct_2['cpu_internal'], 34)
        self.assertEqual(generated_values_correct_3['answer_representation'], '35')
        self.assertEqual(generated_values_correct_3['cpu_representation'], '35')
        self.assertEqual(generated_values_correct_3['cpu_internal'], 35)
        self.assertEqual(generated_values_correct_4['answer_representation'], '150 000 000')
        self.assertEqual(generated_values_correct_4['cpu_representation'], '150 000 000')
        self.assertEqual(generated_values_correct_4['cpu_internal'], 150000000)
        self.assertTrue(generated_values_correct_4['outcome'], True)
        self.assertTrue(generated_values_correct_3['outcome'], True)
        self.assertTrue(generated_values_correct_2['outcome'], True)
        self.assertTrue(generated_values_correct['outcome'], True)
        self.assertTrue(all(element in generated_values_correct for element in self.metadata))

    def test_generate_result_incorrect_values(self):
        interval_incorrect_1 = {
            'left_glyph': '(', 'right_glyph': ')', 'start_internal': 7, 'stop_internal': 41,
            'start_representation': '7', 'stop_representation': '41', 'answer': 38, 'game_level': 0
        }
        interval_incorrect_2 = {
            'left_glyph': '[', 'right_glyph': ']', 'start_internal': 41, 'stop_internal': 7,
            'start_representation': '7', 'stop_representation': '41', 'answer': 35, 'game_level': 0
        }
        interval_incorrect_3 = {
            'left_glyph': '[', 'right_glyph': ']', 'start_internal': 41, 'stop_internal': 7,
            'start_representation': '41', 'stop_representation': '7', 'answer': 35, 'game_level': 0
        }

        # test invalid missing keys
        for key in interval_incorrect_1:
            sample_incorrect_interval = interval_incorrect_1.copy()
            sample_incorrect_interval.pop(key)
            self.assertIsNone(interval_count_game.generate_result(sample_incorrect_interval))

        generated_values_incorrect = interval_count_game.generate_result(interval_incorrect_1)
        generated_values_incorrect_2 = interval_count_game.generate_result(interval_incorrect_2)
        generated_values_incorrect_3 = interval_count_game.generate_result(interval_incorrect_3)
        self.assertEqual(generated_values_incorrect['answer_representation'], '38')
        self.assertEqual(generated_values_incorrect['cpu_representation'], '33')
        self.assertEqual(generated_values_incorrect['cpu_internal'], 33)
        self.assertFalse(generated_values_incorrect['outcome'], False)
        self.assertTrue(all(element in generated_values_incorrect for element in self.metadata))
        self.assertIsNone(generated_values_incorrect_2, None)
        self.assertIsNone(generated_values_incorrect_3, None)

    def test_prettify_number(self):
        self.assertEqual(interval_count_game.prettify_number(100), '100')
        self.assertEqual(interval_count_game.prettify_number(-100), '-100')
        self.assertEqual(interval_count_game.prettify_number(1000), '1 000')
        self.assertEqual(interval_count_game.prettify_number(-1000), '-1 000')
        self.assertEqual(interval_count_game.prettify_number(10000), '10 000')
        self.assertEqual(interval_count_game.prettify_number(-10000), '-10 000')
        self.assertEqual(interval_count_game.prettify_number(100000), '100 000')
        self.assertEqual(interval_count_game.prettify_number(-100000), '-100 000')
        self.assertEqual(interval_count_game.prettify_number(1000000), '1 000 000')
        self.assertEqual(interval_count_game.prettify_number(-1000000), '-1 000 000')
        self.assertEqual(interval_count_game.prettify_number(10000000), '10 000 000')
        self.assertEqual(interval_count_game.prettify_number(-10000000), '-10 000 000')
        self.assertEqual(interval_count_game.prettify_number(100000000), '100 000 000')
        self.assertEqual(interval_count_game.prettify_number(-100000000), '-100 000 000')
        self.assertEqual(interval_count_game.prettify_number(1000000000), '1 000 000 000')
        self.assertEqual(interval_count_game.prettify_number(-1000000000), '-1 000 000 000')
        self.assertEqual(interval_count_game.prettify_number(10000000000), '10 000 000 000')
        self.assertEqual(interval_count_game.prettify_number(-10000000000), '-10 000 000 000')
        self.assertEqual(interval_count_game.prettify_number(100000000000), '100 000 000 000')
        self.assertEqual(interval_count_game.prettify_number(-100000000000), '-100 000 000 000')
