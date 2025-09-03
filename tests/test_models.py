"""
Test model related functionality.

This module encapsulates logic that validates data integrity, relationships
between entities, and database constraints across models.

Classes
-------
UserModelTests
    Test the user entity in various scenarios.
CountryModelTests
    Test the country entity in various scenarios.

Miscellaneous objects
---------------------
Except for the public objects exported by this module and their public
APIs (if applicable), everything else is an implementation detail, and
shouldn't be relied upon as it may change over time.
"""

# Third party
import sqlalchemy
from sqlalchemy import exc

# Project specific
from knowlift.data import models
from tests import factories
from tests import base


class UserModelTests(base.ModelTestCase):
    """
    Test user entity functionality including data integrity and relationships.

    Methods
    -------
    test_select_user
        Verify user record selection by ID.
    test_update_user
        Test user record updates with new values.
    test_create_duplicate_values_for_unique_fields_forbidden
        Ensure unique field constraints prevent duplicate user creation.
    test_update_duplicate_values_for_unique_fields_forbidden
        Ensure unique field constraints prevent duplicate user updates.
    test_create_when_required_fields_are_missing
        Verify required field validation during user creation.
    test_create_user_in_different_country
        Test user creation with custom country association.
    test_methods_in_docstring
        Validate all test methods are documented.
    """

    def setUp(self):
        super().setUp()
        self.user = factories.create_user(self.connection)

    def test_select_user(self):
        where_clause = models.user.c.id == self.user.id
        select_query = sqlalchemy.select(models.user).where(where_clause)
        result = self.connection.execute(select_query).fetchone()

        self.assertEqual(result.id, self.user.id)

    def test_update_user(self):
        data = {
            'username': 'TreeOfLife',
            'email': 'tol@knolift.com',
            'password': 'Yggdrasil'
        }
        where_clause = models.user.c.id == self.user.id
        update_query = models.user.update().where(where_clause).values(data)
        update_result = self.connection.execute(update_query)

        where_clause = models.user.c.username == data['username']
        select_query = sqlalchemy.select(models.user).where(where_clause)
        select_result = self.connection.execute(select_query)
        self.assertEqual(update_result.rowcount, 1)
        self.assertIsNotNone(select_result.fetchone())

    def test_create_duplicate_values_for_unique_fields_forbidden(self):
        test_fields = ('username', 'email')
        for test_field in test_fields:
            payload = {test_field: getattr(self.user, test_field)}

            self.assertRaises(
                exc.IntegrityError,
                factories.create_user,
                self.connection,
                **payload
            )

    def test_update_duplicate_values_for_unique_fields_forbidden(self):
        test_fields = ('username', 'email')
        user = factories.create_user(self.connection)
        for test_field in test_fields:
            data = {test_field: getattr(self.user, test_field)}
            where_clause = models.user.c.id == user.id
            update_query = models.user.update().where(where_clause).values(data)

            self.assertRaises(
                exc.IntegrityError,
                self.connection.execute,
                update_query
            )

    def test_create_when_required_fields_are_missing(self):
        required_fields = ('username', 'email', 'password', 'country_id')
        for required_field in required_fields:
            payload = {required_field: None}

            self.assertRaises(
                exc.IntegrityError,
                factories.create_user,
                self.connection,
                **payload
            )

    def test_create_user_in_different_country(self):
        payload = {
            'english_short_name': 'Australia',
            'alpha2_code': 'AU',
            'alpha3_code': 'AUS'
        }
        country_name = payload['english_short_name']
        where_clause = models.country.c.english_short_name == country_name
        select_query = sqlalchemy.select(models.country).where(where_clause)

        self.assertIsNone(self.connection.execute(select_query).fetchone())

        user = factories.create_user(self.connection, **payload)

        select_query = sqlalchemy.select(
            models.user.c.username,
            models.country.c["english_short_name", "alpha2_code", "alpha3_code"]
        ).where(
            models.user.c.username == user.username
        ).join(
            models.country,
            models.user.c.country_id == models.country.c.id
        )
        result = self.connection.execute(select_query).fetchone()

        self.assertTrue(
            all(payload[key] == getattr(result, key) for key in payload.keys())
        )

    def test_methods_in_docstring(self):
        methods_to_check = [
            method_name for method_name in dir(self)
            if method_name.startswith('test')
        ]
        for method_to_check in methods_to_check:
            msg = f'{method_to_check} not found in docstring.'

            self.assertIn(method_to_check, self.__doc__, msg)

    def tearDown(self):
        count = sqlalchemy.func.count()
        select_query = sqlalchemy.select(count).select_from(models.user)
        count_result = self.connection.execute(select_query).fetchone()
        delete_query = models.user.delete()
        delete_result = self.connection.execute(delete_query)

        self.assertEqual(count_result.count_1, delete_result.rowcount)
        super().tearDown()


class CountryModelTests(base.ModelTestCase):
    """
    Test country entity functionality including data integrity and validation.

    Methods
    -------
    test_select_country
        Verify country record selection by ID.
    test_update_country
        Test country record updates with new values.
    test_create_duplicate_values_for_unique_fields_forbidden
        Ensure unique field constraints prevent duplicate country creation.
    test_update_duplicate_values_for_unique_fields_forbidden
        Ensure unique field constraints prevent duplicate country updates.
    test_create_when_required_fields_are_missing
        Verify required field validation during country creation.
    test_create_record_max_length_exceeded
        Test field length constraints on country codes.
    test_methods_in_docstring
        Validate all test methods are documented.
    """

    def setUp(self):
        super().setUp()
        self.country = factories.create_country(self.connection)

    def test_select_country(self):
        where_clause = models.country.c.id == self.country.id
        select_query = sqlalchemy.select(models.country).where(where_clause)
        result = self.connection.execute(select_query).fetchone()

        self.assertEqual(result.id, self.country.id)

    def test_create_duplicate_values_for_unique_fields_forbidden(self):
        test_fields = {
            'english_short_name': 'United States of America',
            'alpha2_code': 'US',
            'alpha3_code': 'USA',
        }
        # When we're popping a value, we're using the default value from the
        # factory for that value
        for key in test_fields:
            test_fields_copy = dict(test_fields)
            test_fields_copy.pop(key)

            self.assertRaises(
                exc.IntegrityError,
                factories.create_country,
                self.connection,
                **test_fields_copy
            )

    def test_update_country(self):
        data = {
            'english_short_name': 'United States of America',
            'alpha2_code': 'US',
            'alpha3_code': 'USA',
        }

        where_clause = models.country.c.id == self.country.id
        update_query = models.country.update().where(where_clause).values(data)
        update_result = self.connection.execute(update_query)

        country_name = data['english_short_name']
        name_clause = models.country.c.english_short_name == country_name
        select_query = sqlalchemy.select(models.country).where(name_clause)
        select_result = self.connection.execute(select_query).fetchone()

        self.assertEqual(update_result.rowcount, 1)
        self.assertIsNotNone(select_result)

    def test_update_duplicate_values_for_unique_fields_forbidden(self):
        new_values = {
            'english_short_name': 'United States of America',
            'alpha2_code': 'US',
            'alpha3_code': 'USA',
        }
        country = factories.create_country(self.connection, **new_values)
        for field in models.country.c.keys():
            d = {field: getattr(self.country, field)}
            where_clause = models.country.c.id == country.id
            update_query = models.country.update().where(where_clause).values(d)

            self.assertRaises(
                exc.IntegrityError,
                self.connection.execute,
                update_query
            )

    def test_create_when_required_fields_are_missing(self):
        required_fields = ('english_short_name', 'alpha2_code', 'alpha3_code')
        for required_field in required_fields:
            payload = {required_field: None}

            self.assertRaises(
                exc.IntegrityError,
                factories.create_country,
                self.connection,
                **payload
            )

    def test_create_record_max_length_exceeded(self):
        alpha2 = {
            'english_short_name': 'Germany',
            'alpha2_code': 'ALPHA',
            'alpha3_code': 'DEU'
        }
        alpha3 = {
            'english_short_name': 'Germany',
            'alpha2_code': 'DE',
            'alpha3_code': 'OMEGA'
        }
        self.assertRaises(
            exc.IntegrityError,
            factories.create_country,
            self.connection,
            **alpha2
        )
        self.assertRaises(
            exc.IntegrityError,
            factories.create_country,
            self.connection,
            **alpha3
        )

    def test_methods_in_docstring(self):
        methods_to_check = [
            method_name for method_name in dir(self)
            if method_name.startswith('test')
        ]
        for method_to_check in methods_to_check:
            msg = f'{method_to_check} not found in docstring.'

            self.assertIn(method_to_check, self.__doc__, msg)

    def tearDown(self):
        count = sqlalchemy.func.count()
        select_query = sqlalchemy.select(count).select_from(models.country)
        count_result = self.connection.execute(select_query).fetchone()
        delete_query = models.country.delete()
        delete_result = self.connection.execute(delete_query)

        self.assertEqual(count_result.count_1, delete_result.rowcount)
        super().tearDown()
