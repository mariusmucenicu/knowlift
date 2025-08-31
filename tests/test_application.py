# SPDX-FileCopyrightText: 2024 (C) Marius Mucenicu
# SPDX-License-Identifier: AGPL-3.0-or-later


"""
Test application layer functionality.

Classes
-------
IntervalCountGameTests
    Test the interval counting game application services.

Miscellaneous objects
---------------------
Except for the public objects exported by this module and their public
APIs (if applicable), everything else is an implementation detail, and
shouldn't be relied upon as it may change over time.
"""

# Standard library
import unittest

# Project specific
from knowlift.application import interval_count


class IntervalCountGameTests(unittest.TestCase):
    """
    Test interval counting game application services.

    Methods
    -------
    test_start_game_valid_level
        Test game initiation with valid difficulty level.
    test_start_game_invalid_level
        Test game initiation with invalid difficulty level.
    test_evaluate_answer_valid_data
        Test answer evaluation with valid game data.
    test_evaluate_answer_invalid_data
        Test answer evaluation with invalid game data.
    """

    def test_start_game_valid_level(self):
        """Test game initiation with valid difficulty level."""
        result = interval_count.start_game('0')
        
        self.assertIsNotNone(result)
        self.assertIn('left_glyph', result)
        self.assertIn('right_glyph', result)
        self.assertIn('start_internal', result)
        self.assertIn('stop_internal', result)
        self.assertIn('game_level', result)

    def test_start_game_invalid_level(self):
        """Test game initiation with invalid difficulty level."""
        result = interval_count.start_game('invalid')
        
        self.assertIsNone(result)

    def test_evaluate_answer_valid_data(self):
        """Test answer evaluation with valid game data."""
        test_data = {
            'left_glyph': '[',
            'right_glyph': ']',
            'start_internal': 5,
            'stop_internal': 10,
            'start_representation': '5',
            'stop_representation': '10',
            'answer': 6,
            'game_level': 0
        }
        
        result = interval_count.evaluate_answer(test_data)
        
        self.assertIsNotNone(result)
        self.assertIn('outcome', result)
        self.assertIn('cpu_internal', result)
        self.assertEqual(result['outcome'], True)

    def test_evaluate_answer_invalid_data(self):
        """Test answer evaluation with invalid game data."""
        test_data = {'invalid': 'data'}
        
        result = interval_count.evaluate_answer(test_data)
        
        self.assertIsNone(result)
