"""
Test web related functionality (views, templates, overall interaction, etc.)

CONSTANTS:
==========
    HTTP_CLIENT: A Python class that acts as a dummy Web browser, allowing you to test your views.

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
import unittest

# Project specific
import tests

HTTP_CLIENT = tests.TEST_APPLICATION.test_client()


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

