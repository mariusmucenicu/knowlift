# SPDX-FileCopyrightText: 2024 (C) Marius Mucenicu
# SPDX-License-Identifier: AGPL-3.0-or-later


"""
Implement a way to build valid independent clauses (simple sentences).

This module encapsulates the logic for working with a given Lexicon and build valid, simple
Sentence(s) from that Lexicon.

Classes:
========
    Lexicon: Identify words against a given lexicon.
    Sentence: Build basic sentences following a word order rule, e.g SVO (Subject Verb Object).
    ParserError: Raise when trying to build invalid Sentence(s).

Functions:
==========
    check_ascii: Check whether a given string is valid ASCII. UTF-8 encoding works as well since
        it's a superset of ASCII, but the characters must be within the ASCII range.

Miscellaneous objects:
======================
    Except for the public objects exported by this module and their public APIs (if applicable),
        everything else is an implementation detail, and shouldn't be relied upon as it may change
        over time.
"""

__author__ = 'Marius Mucenicu <marius_mucenicu@yahoo.com>'


def check_ascii(raw_string):
    """Checks whether all the characters in an input string are ASCII compatible"""
    assert raw_string, 'invalid call with no data'
    return all(ord(letter) < 127 for letter in raw_string)


class ParserError(Exception):
    """Custom exception for dealing with invalid Sentence types"""
    pass


class Lexicon:
    """
    Methods:
    ========
        scan_text()
        split_alphanum()
        validate()
    """

    def __init__(self, wordbook):
        """
        Initialize a new Lexicon object.

        Args:
            :param wordbook (dict): Words, representing the lexicon of a particular subject.

        Example:
            The wordbook must have the following form:
            {'part_of_speech' : {value1, value2, value3, etc.}}

            {'subject': {'player', 'showman', 'etc'},
             'verb': {'go', 'run', 'etc'},
             'object': {'door', 'vault', 'etc'},
             'constituent': {'in', 'at', 'etc'}}
        """
        # class invariants
        assert wordbook, 'cannot operate on empty dictionary'
        assert self.validate(wordbook), 'invalid lexicon'
        self.wordbook = wordbook

    def validate(self, wordbook):
        """
        Check whether the wordbook provided has unique lowercase words with just alpha chars.

        Args:
            :param wordbook (dict): A lexicon (vocabulary/dictionary).

        Returns:
            True (bool) if all checks have passed successfully.

        Raises:
            AssertionError:
                If the word categories (parts of speech) are greater than 64.
                If any word category contains: uppercase, non-valid-ASCII chars, non-alpha chars, or
                    is not of type string.
                If the values associated with each category is not a set.
                If the words comprising the lexicon contain: uppercase, non-valid-ASCII chars,
                    non-alpha chars, or are not of type string.
                If there are duplicates hidden amongst different categories.
        """
        # TODO(Marius): also check the parts of speech against the acknowledged classification
        assert len(wordbook) <= 64, 'too many parts of speech (word categories) in the lexicon'
        assert all(
            term.isalpha() and term.islower() and check_ascii(term) for term in wordbook.keys()
        ), 'invalid word type or format within keys'

        checked_words = set()
        for word_set in wordbook.values():
            assert word_set, 'empty data set not allowed'
            assert all(
                word.isalpha() and word.islower() and check_ascii(word) for word in word_set
            ), 'invalid word found in {0}'.format(word_set)

            if word_set & checked_words:
                assert False, 'duplicate entries for words {0}'.format(word_set & checked_words)
            else:
                checked_words.update(word_set)
        return True

    def split_alphanum(self, raw_string):
        """
        Parses a raw string and remove any non alphanumeric characters out of it.

        Args:
            :param raw_string (str): An unformatted, raw text.

        Returns:
            A list of formatted words (lowercase, special characters removed) and/or numbers.

        Raises:
            AssertionError:
                If words are not composed entirely out of alphabetic characters like: 'the', 'king',
                'deuce' or entirely out of digits: '1990', '2079'. Bad (would raise): 'th3', 'k1ng'.
        """
        assert len(raw_string) <= 512, 'maximum input length of 512 characters exceeded'

        special_characters = {
            letter
            for letter in raw_string
            if not (letter.isalnum() or letter.isspace())
        }
        punctuation_marks = {'.', ',', '?', '!', "'", '"', ':', ';', '-'}

        for character in special_characters:
            if character not in punctuation_marks:
                raw_string = raw_string.replace(character, '')
            else:
                raw_string = raw_string.replace(character, ' ')

        words = raw_string.lower().split()
        assert all(word.isalpha() or word.isdigit() for word in words), 'alphanumeric words found'
        return words

    def scan_text(self, raw_string):
        """
        Scan a text and match words against a lexicon to identify each word's class

        Args:
            :param raw_string (str): An unformatted, raw text.

        Returns:
            A list of processed words where each word from the input string, has been identified
            and labeled with a word class from a given lexicon, or the 'error' class if it could not
            be found.
        """
        assert raw_string, 'invalid call with no data'
        assert check_ascii(raw_string), 'invalid characters'

        processed_words = []
        words = self.split_alphanum(raw_string)

        for word in words:
            processed = False
            for key, value in self.wordbook.items():
                if word in value:
                    processed_words.append((key, word))
                    processed = True
            if not processed:
                processed_words.append(('error', word))
        return processed_words


class Sentence:
    """
    Methods:
    ========
        build()
    """

    def __init__(self, word_order):
        """
        Initialize a new Sentence object.

        Args:
            :param word_order (str): Represents the rule upon which sentences will built.

        Notes:
            The most popular, acknowledged word orders are:
                * Subject Verb Object (SVO),
                * Subject Object Verb (SOV),
                * Verb Subject Object (VSO),
            All together they account for more than 85% of the world's languages
        """
        # class invariants
        word_order = word_order.strip().lower()
        assert word_order in ('svo', 'sov', 'vso'), 'invalid word order'

        word_pattern = {
            'svo': ('subject', 'verb', 'object'),
            'sov': ('subject', 'object', 'verb'),
            'vso': ('verb', 'subject', 'object'),
        }
        self.expected_order = word_pattern[word_order]

    def build(self, words):
        """
        Build a simple sentence (one independent clause) based on the word order.

        Args:
            :param words (list): Contains 2 item tuples of the form ('token', 'word')

        Returns:
            A simple sentence with the identified words from the lexicon, given a word order.

        Raises:
            ParserError:
                If the word to be appended to the sentence is not an expected word.
                Example: If the word order is: SVO (Subject Verb Object) it expects a Subject first.
                    If you give it a sentence like Smack the bear, it will raise an exception.

        Notes:
            Constituents from the lexicon are ignored in order to build a variety of sentences with
                a small vocabulary.
            Example: Punch the bear in the face will yield Punch bear face.
        """
        assert words, 'invalid call with no data'
        assert all(len(pair) == 2 for pair in words), 'unequal (token, word) pairs'

        position = 0
        sentence = []

        for token, word in words:
            if token == 'constituent':
                continue
            elif token == self.expected_order[position]:
                sentence.append(word)
                if position + 1 >= len(self.expected_order):
                    return ' '.join(sentence)
                else:
                    position += 1
            else:
                raise ParserError(
                    'Expected {0} but got {1}'.format(self.expected_order[position], token)
                )
