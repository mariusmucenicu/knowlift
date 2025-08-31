# SPDX-FileCopyrightText: 2024 (C) Marius Mucenicu
# SPDX-License-Identifier: AGPL-3.0-or-later


"""
Interval counting game workflows.

Functions
---------
start_game
    Initiate a new game round based on difficulty level.
evaluate_answer
    Process and evaluate a player's answer.

Notes
-----
Except for the public objects exported by this module and their public APIs
(if applicable), everything else is an implementation detail and should not be
relied upon, as it may change over time.
"""

# Project specific
from knowlift.domain import interval_count_game


def start_game(level):
    """
    Initiate a new game round for the specified difficulty level.
    
    :param level: Difficulty level for the game round.
    :type level: str
    :return: Game data containing interval information, or None if invalid.
    :rtype: dict | None
    """
    return interval_count_game.play(level)


def evaluate_answer(data):
    """
    Process and evaluate a player's answer against the expected result.
    
    :param data: Game data containing player's answer and interval metadata.
    :type data: dict
    :return: Result data with outcome and statistics, or None if invalid.
    :rtype: dict | None
    """
    return interval_count_game.generate_result(data)
