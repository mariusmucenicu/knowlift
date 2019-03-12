"""
Implement the interface for a simple mathematical game based on intervals.

Functions:
==========
    calculate_statistics: Compute statistics based on amount of correct/incorrect answers.
    change_game_level: Increment/decrement the degree of difficulty based on statistics.
    fetch_game_level: Return a game level from a series of game levels, based on user preference.
    generate_interval: Generate an interval within a range of two values (the lower/upper bound).
    generate_results: Compare the user's result with the expected result for a given question.
    play: Entry point for the game.
    prettify_number: Split large numbers into groups of three digits to aid readability.
    validate_form_data: Ensure the data passed in through the form matches an expected format.
    validate_game_levels: Ensure the game levels respect certain criteria.

CONSTANTS:
==========
    GAME_LEVELS: A series of available game levels ranging in difficulty.

Miscellaneous objects:
======================
    Except the above, all other objects in this module are to be considered implementation details.
"""

__author__ = 'Marius Mucenicu <marius_mucenicu@yahoo.com>'

# Standard library
import logging
import random

logger = logging.getLogger(__name__)

GAME_LEVELS = (
    (0, 10**2 - 1),
    (-10**2 + 1, 10**2 - 1),
    (0, 10**3 - 1),
    (-10**3 + 1, 10**3 - 1),
    (0, 10**4 - 1),
    (-10**4 + 1, 10**4 - 1),
    (0, 10**5 - 1),
    (-10**5 + 1, 10**5 - 1),
    (0, 10**6 - 1),
    (-10**6 + 1, 10**6 - 1),
    (0, 10**9 - 1),
    (-10**9 + 1, 10**9 - 1),
)


def calculate_statistics(correct, incorrect):
    """
    Compute the statistics based on the total number of correct and incorrect answers.

    Args:
        :param correct (int): Number of correct answers.
        :param incorrect (int): Number of incorrect answers.

    Returns:
        A tuple of length 3 of the form:
            (total number of answers, correct percentage, incorrect percentage)
    """
    total = correct + incorrect
    correct_percentage = round(correct / total * 100, 2)
    incorrect_percentage = round(100 - correct_percentage, 2)
    return correct_percentage, incorrect_percentage


def change_game_level(avg_correct, avg_incorrect, game_level):
    """
    Increase or decrease the game difficulty level based on the success rate.

    Args:
        :param avg_correct (int): Number of correct answers.
        :param avg_incorrect (int): Number of incorrect answers.
        :param game_level (int): Number representing the current degree of difficulty.

    Returns:
        An int, corresponding to the position of the current game level in GAME_LEVELS.
    """

    game_levels = len(GAME_LEVELS)
    correct_percentage = calculate_statistics(avg_correct, avg_incorrect)[0]

    if correct_percentage >= 50:
        if game_level + 1 < game_levels:
            game_level += 1
        else:
            logger.info('Maximum level reached')
    elif game_level:
        game_level -= 1
    else:
        logger.info('Minimum level reached')
    return game_level


def fetch_game_level(user_input):
    """
    Fetch a particular game level based on a given input.

    Args:
        :param user_input (str): A cardinal number used to extract a game level from a tuple.

    Returns:
        A tuple of length 2 of the form:
            (lower_bound, upper_bound)
    """
    try:
        game_level = int(user_input.strip())
    except ValueError as ex:
        logger.exception(ex)
        return None

    if validate_game_levels(GAME_LEVELS) and 0 <= game_level < len(GAME_LEVELS):
        return GAME_LEVELS[game_level]
    else:
        logger.error('Unable to fetch the game level with index: %s', game_level)
        return None


def generate_interval(game_level):
    """
    Generate an interval within two limits.

    Args:
        :param game_level (tuple): Upper/lower bound values from which an interval is built.

    Returns:
        A dictionary comprising the 'raw data' (metadata) used to create the mathematical interval.
    """
    if game_level is None:
        return game_level
    else:
        start_value = game_level[0]
        stop_value = game_level[1]
        left_glyphs, right_glyphs = ('[', '('), (']', ')')
        start = random.randint(start_value, stop_value)
        stop = random.randint(start, stop_value)
        left_glyph = random.choice(left_glyphs)
        right_glyph = random.choice(right_glyphs)

        data = {
            'left_glyph': left_glyph,
            'right_glyph': right_glyph,
            'start_internal': start,
            'stop_internal': stop,
            'start_representation': prettify_number(start),
            'stop_representation': prettify_number(stop),
            'game_level': GAME_LEVELS.index(game_level),
        }
        return data


def generate_results(data):
    """
    Generate results based on a mathematical interval as well as a user's answer.

    Args:
        :param data (dict): A mapping containing metadata about a particular game question.

    Returns:
        A dict comprising the initial data plus the result of comparing a user's answer with the
        expected result.

    """

    if validate_form_data(data):
        answer = data.get('answer')
        left_glyph = data.get('left_glyph')
        right_glyph = data.get('right_glyph')
        start = data.get('start_internal')
        stop = data.get('stop_internal')

        if left_glyph == '[' and right_glyph == ']':
            cpu_result = len(range(start, stop + 1))
        elif left_glyph == '(' and right_glyph == ')':
            cpu_result = len(range(start, stop - 1))
        else:
            cpu_result = len(range(start, stop))

        data['cpu_internal'] = cpu_result
        data['cpu_representation'] = prettify_number(cpu_result)
        data['answer_representation'] = prettify_number(answer)
        data['outcome'] = cpu_result == answer
        return data
    else:
        return None


def play(user_input):
    """
    Start the game.

    Args:
        :param user_input (str): A value corresponding to a game level.

    Returns:
        See generate_interval's function for the return value.
    """
    game_level = fetch_game_level(user_input)
    return generate_interval(game_level)


def prettify_number(number):
    """
    Make numbers greater than 100 more readable by grouping into groups of 3 digits.

    Example:
        1000 -> 1 000
        65536 -> 65 536
        1000000 -> 1 000 000

    Args:
        :param number (int): Number to be formatted.

    Returns:
        A string representation of the number prettily formatted.
    """
    number = str(number)
    if len(number) <= 3:
        return number
    else:
        raw_formatted_number = []
        slice_stop = len(number)

        for slice_start in range(-3, -len(number), -3):
            three_chunk = number[slice_start:slice_stop]
            raw_formatted_number.insert(0, three_chunk)
            slice_stop = slice_start

            if slice_start - 3 <= -len(number):
                raw_formatted_number.insert(0, number[:slice_start])

        if raw_formatted_number[0] == '-':
            raw_formatted_number[:2] = [raw_formatted_number[0] + raw_formatted_number[1]]

        pretty_formatted_number = ' '.join(raw_formatted_number)
        return pretty_formatted_number


def validate_form_data(form_data):
    """
    Make sure the form data passed in respects a certain format.

    Args:
        :param form_data (dict): Data passed through form.

    Returns:
        True for valid data, None for invalid data.

    Notes:
        This validation only ensures that the data format is consistent with what the game expects.
        It does not ensure that the values are unaltered and as a consequence one could easily trick
        the game and pass all the quiz questions by sending in desired mathematical intervals with
        numbers that match the size of those intervals.
    """
    expected_glyphs = {'left_glyph': ('[', '('), 'right_glyph': (']', ')')}
    expected_numbers = (
        'start_internal', 'stop_internal', 'start_representation', 'stop_representation', 'answer',
        'game_level',
    )
    internal_values = []
    representation_values = []

    for glyph, value in expected_glyphs.items():
        if glyph not in form_data:
            logger.error('%s not found in form data.', glyph)
            return None
        elif form_data[glyph] not in value:
            logger.error('unexpected glyph %s', form_data[glyph])
            return None

    for number in expected_numbers:
        if number not in form_data:
            logger.error('%s not found in form data.', number)
            return None
        else:
            try:
                if isinstance(form_data[number], str) and 'representation' in number:
                    form_value = form_data[number].replace(' ', '')
                    representation_values.append(int(form_value))
                elif isinstance(form_data[number], int) and 'internal' in number:
                    form_value = form_data[number]
                    internal_values.append(int(form_value))
                else:
                    int(form_data[number])
            except (TypeError, ValueError) as ex:
                logger.exception(ex)
                return None

    lower_bound = internal_values[0]
    upper_bound = internal_values[1]
    no_values = not (internal_values and representation_values)

    if no_values or internal_values != representation_values or lower_bound > upper_bound:
        logger.error(
            'inconsistency among numbers'
            '\tinternal values: %s'
            ' != representation values: %s', internal_values, representation_values
        )
        return None
    else:
        return True


def validate_game_levels(game_levels):
    """
    Validate a set of game levels against a set of rules.

    Args:
        :param game_levels (tuple): A series of game levels.

    Returns:
        A boolean object: True if all game levels are valid, False otherwise.

    Notes:
        Game levels should meet the following 2 criteria:
        1. Should be unique across the entire levels (not having a level appear multiple times).
        2. The game difficulties themselves should be valid mathematical intervals, i.e the lower
            bound should not be greater than the upper bound.
    """

    if not len(set(game_levels)) == len(game_levels):
        return False
    else:
        for lower_bound, upper_bound in game_levels:
            if lower_bound > upper_bound:
                return False
        return True
