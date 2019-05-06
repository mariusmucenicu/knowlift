"""
Test web related functionality (views, templates, overall interaction, etc.)

CONSTANTS:
==========
    HTTP_CLIENT: A Python class that acts as a dummy Web browser, allowing you to test your views.
    TEST_APPLICATION: A Python class which implements a WSGI application and acts as a central obj.

Functions:
==========
    check_membership: Check if all the elements of a given array are found in a target string.

Classes:
========
    TestIndexPage: Test the requests going under /index
    TestAboutPage: Test the requests going under /about
    TestCustomInternalErrorPage: Test the requests that the server failed to fulfil
    TestCustomNotFoundPage: Test the requests that are not mapped to any URL
    TestGradePage: Test the requests going under /grade
    TestLadderPage: Test the requests going under /ladder
    TestLegalPage: Test the requests going under /legal
    TestPlayPage: Test the requests going under /play
    TestResultPage: Test the requests going under /result
"""

# Standard library
import json
import unittest

# Project specific
import knowlift

from knowlift import default_settings

TEST_APPLICATION = knowlift.create_app(default_settings.__file__)
HTTP_CLIENT = TEST_APPLICATION.test_client()


def check_membership(text, *strings):
    """Check whether all elements of a sequence are in a given text."""
    for element in strings:
        assert element in text, f'Body does not contain the string {element}.'
    return True


class TestIndexPage(unittest.TestCase):
    """
    Methods:
    ========
        test_get_index_page()
    """

    def test_get_index_page(self):
        response = HTTP_CLIENT.get('/')
        response_body = response.get_data(as_text=True)
        expected_items = (
            'Welcome to the fascinating world of arithmetic',
            'This game aims to mimic the behavior of an abacus',
            'open interval',
            'closed interval',
            'half-open interval',
            'container-fluid d-flex flex-column',
            'd-flex flex-column justify-content-center',
            '...Shh',
            'A pit stop for your brain.',
            'Version 1.0.0',
            'header',
            'content',
            'footer',
            'https://www.w3.org/TR/html/',
            'https://www.w3.org/TR/CSS/',
            'https://www.w3schools.com/js/js_versions.asp',
            'https://www.python.org/',
            'Connect with the author:',
            'twitter',
            'instagram',
            'linkedin',
            'github',
        )
        expected_items_in_body = check_membership(response_body, *expected_items)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(expected_items_in_body)


class TestAboutPage(unittest.TestCase):
    """
    Methods:
    ========
        test_get_about_page()
    """

    def test_get_about_page(self):
        response = HTTP_CLIENT.get('/about')
        response_body = response.get_data(as_text=True)
        expected_items = (
            'About',
            '/about',
            'coming_soon',
        )
        expected_items_in_body = check_membership(response_body, *expected_items)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(expected_items_in_body)


class TestCustomInternalErrorPage(unittest.TestCase):
    """
    Methods:
    ========
        test_yield_custom_internal_error_page()
    """

    def setUp(self):
        self.payload = {
            'left_glyph': '[',
            'right_glyph': ')',
            'start_internal': 0,
            'stop_internal': 99,
            'start_representation': '0',
            'stop_representation': '99',
            'answer': 'bogus',  # only integers allowed
            'game_level': 0,
        }

    def test_yield_custom_internal_error_page(self):
        data = {'data': json.dumps(self.payload)}
        response = HTTP_CLIENT.post('/result', data=data)
        response_body = response.get_data(as_text=True)
        expected_items = (
            'Oops! It looks like',
            "Try that again, and if it still doesn't work",
            'Below you will find two helpful links. You know, just in case.',
            'Home page',
            "Nah bruh. I'm outta here!",
            'type="image/webp"',
            'dinosaur_slim.webp',
            'dinosaur.jpg',
        )
        expected_items_in_body = check_membership(response_body, *expected_items)
        self.assertEqual(response.status_code, 500)
        self.assertTrue(expected_items_in_body)


class TestCustomNotFoundPage(unittest.TestCase):
    """
    Methods:
    ========
        test_get_custom_not_found_page()
    """

    def test_get_custom_not_found_page(self):
        response = HTTP_CLIENT.get('/bogus')
        response_body = response.get_data(as_text=True)
        expected_items = (
            'Oops! It looks like',
            "Looks like you followed a bad path. If you think it's the author's fault",
            'Below you will find two helpful links. You know, just in case.',
            'Home page',
            "Nah bruh. I'm outta here!",
            'type="image/webp"',
            'detective_slim.webp',
            'detective.jpg',
        )
        expected_items_in_body = check_membership(response_body, *expected_items)
        self.assertEqual(response.status_code, 404)
        self.assertTrue(expected_items_in_body)


class TestGradePage(unittest.TestCase):
    """
    Methods:
    ========
        test_get_grade_page()
    """

    def test_get_grade_page(self):
        response = HTTP_CLIENT.get('/grade')
        response_body = response.get_data(as_text=True)
        expected_items = (
            'Please choose one of the following difficulties',
            'Easy',
            'Medium',
            'Hard',
            'Use selected',
            'Just pick one for me',
            'Numberphile',
            'Warm up',
            'Numbers are my thing',
            'God blessed my genes',
            'd-flex flex-column justify-content-center',
        )
        expected_items_in_body = check_membership(response_body, *expected_items)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(expected_items_in_body)


class TestLadderPage(unittest.TestCase):
    """
    Methods:
    ========
        test_get_ladder_page()
    """

    def test_get_ladder_page(self):
        response = HTTP_CLIENT.get('/ladder')
        response_body = response.get_data(as_text=True)
        expected_items = (
            'Ladder',
            '/ladder',
            'coming_soon.jpg',
        )
        expected_items_in_body = check_membership(response_body, *expected_items)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(expected_items_in_body)


class TestLegalPage(unittest.TestCase):
    """
    Methods:
    ========
        test_get_legal_page()
    """

    def test_get_legal_page(self):
        response = HTTP_CLIENT.get('/legal')
        response_body = response.get_data(as_text=True)
        expected_items = (
            'border-stretch',
            'contents',
            'contents__item',
            'contents__link',
            'legal__terms_conditions',
            'legal__liability',
            'legal__litigation',
            'legal__privacy_policy',
            'legal__data_security',
            'legal__do_not_track',
            'legal__cookie_policy',
            'legal__cookie_types',
            'legal__cookie_usage',
            'legal__cookie_ctrl',
            'legal__cookie_extra_info',
            'legal__additional_info',
            'legal__app_history',
            'legal__license',
            'legal__useful_links',
            'fa-chevron-circle-up',
            'marius_mucenicu@yahoo.com',
            'mariusmucenicu',
            'Marius Mucenicu',
            'scrollToElement',
        )
        expected_items_in_body = check_membership(response_body, *expected_items)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(expected_items_in_body)


class TestPlayPage(unittest.TestCase):
    """
    Methods:
    ========
        test_get_not_allowed()
        test_play_post_with_incorrect_values()
        test_play_post_valid_data()
    """

    def test_get_not_allowed(self):
        response = HTTP_CLIENT.get('/play')
        self.assertEqual(response.status_code, 405)

    def test_play_post_with_incorrect_values(self):
        invalid_values = ('a', 12)
        for value in invalid_values:
            response = HTTP_CLIENT.post('/play', data={'level': value})
            response_body = response.get_data(as_text=True)
            expected_items = (
                'Oops! It looks like',
                "Try that again, and if it still doesn't work",
                'Below you will find two helpful links. You know, just in case.',
                'Home page',
                "Nah bruh. I'm outta here!",
                'type="image/webp"',
                'dinosaur_slim.webp',
                'dinosaur.jpg',
            )
            expected_items_in_body = check_membership(response_body, *expected_items)
            self.assertEqual(response.status_code, 500)
            self.assertTrue(expected_items_in_body)

    def test_play_post_valid_data(self):
        data = {'level': 0}
        response = HTTP_CLIENT.post('/play', data=data)
        response_body = response.get_data(as_text=True)
        expected_items = (
            'Submit answer',
            "I'm feeling lucky",
            'How many integers are within this interval ?',
            'd-flex flex-column justify-content-center',
            'checkEmptyInput',
            'processFormData',
            'clearFormField',
            'fa-times',
            'fa-search',
            'metadata',
            'play-form',
            'form-play',
            'roulette',
            'clearSearch',
            'play-form__input',
            'form-play__button',
            'form-play__button--glass',
            'form-play__button--toggle',
        )
        expected_items_in_body = check_membership(response_body, *expected_items)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(expected_items_in_body)


class TestResultPage(unittest.TestCase):
    """
    Methods:
    ========
        test_post_result_correct_answer()
        test_result_get_not_allowed()
        test_post_result_incorrect_answer()
        test_post_erroneous_data()
    """

    def setUp(self):
        self.post_data = {
            'left_glyph': '[',
            'right_glyph': ')',
            'start_internal': 0,
            'stop_internal': 99,
            'start_representation': '0',
            'stop_representation': '99',
            'answer': 99,
            'game_level': 0,
        }

    def test_post_result_correct_answer(self):
        data = {'data': json.dumps(self.post_data)}
        response = HTTP_CLIENT.post('/result', data=data)
        response_body = response.get_data(as_text=True)
        expected_items = (
            'Correct!',
            'Next question',
            "I'm done for today",
            'd-flex flex-column justify-content-center',
        )
        expected_items_in_body = check_membership(response_body, *expected_items)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(expected_items_in_body)

    def test_result_get_not_allowed(self):
        response = HTTP_CLIENT.get('/result')
        self.assertEqual(response.status_code, 405)

    def test_post_result_incorrect_answer(self):
        incorrect_values = {
            'start_internal': 299792458,
            'stop_internal': 299792459,
            'start_representation': '299 792 458',
            'stop_representation': '299 792 459',
        }
        self.post_data.update(incorrect_values)
        data = {'data': json.dumps(self.post_data)}
        response = HTTP_CLIENT.post('/result', data=data)
        response_body = response.get_data(as_text=True)
        expected_items = (
            'Incorrect!',
            'Next question',
            "I'm done for today",
            'd-flex flex-column justify-content-center',
            'Interval',
            'Your answer',
            'Correct answer',
            '299 792 458',
            '299 792 459',
        )
        expected_items_in_body = check_membership(response_body, *expected_items)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(expected_items_in_body)

    def test_post_erroneous_data(self):
        erroneous_values = {
            'left_glyph': ']',
            'right_glyph': '(',
            'start_representation': '5',
            'answer': 'bogus',
            'game_level': '',
        }
        self.post_data.update(erroneous_values)
        data = {'data': json.dumps(self.post_data)}
        response = HTTP_CLIENT.post('/result', data=data)
        response_body = response.get_data(as_text=True)
        expected_items = (
            'Oops! It looks like',
            "Try that again, and if it still doesn't work",
            'Below you will find two helpful links. You know, just in case.',
            'Home page',
            "Nah bruh. I'm outta here!",
            'type="image/webp"',
            'dinosaur_slim.webp',
            'dinosaur.jpg',
        )
        expected_items_in_body = check_membership(response_body, *expected_items)
        self.assertEqual(response.status_code, 500)
        self.assertTrue(expected_items_in_body)
