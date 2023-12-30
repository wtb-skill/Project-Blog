# import pytest
# from blog import app, db as _db
# from flask import url_for
# from flask_migrate import upgrade as _upgrade
# from blog.models import Entry
#
#
# @pytest.fixture
# def logged_in_client():
#     with app.test_client() as client:
#         with client.session_transaction() as session:
#             session['logged_in'] = True
#         yield client
#
#
# @pytest.fixture
# def logged_out_client():
#     with app.test_client() as client:
#         with client.session_transaction() as session:
#             session['logged_in'] = False
#         yield client
#
#
# @pytest.fixture(scope="session")
# def test_app():
#     app.config.from_object("config.TestConfig")  # Use a separate test config
#     with app.app_context():
#         _db.create_all()  # Create the test database
#         _upgrade()  # Apply migrations
#
#     yield app
#
#     # Teardown - drop all tables and remove the test database
#     with app.app_context():
#         _db.session.remove()
#         _db.drop_all()
#
#
# def test_delete_entry(logged_in_client, test_app):
#     with test_app.app_context():  # Activate the app context for database operations
#         # Create an entry
#         entry = Entry(title='Test Title', body='Test Body', is_published=True)
#         _db.session.add(entry)
#         _db.session.commit()
#
#         # Get the entry ID for deletion
#         entry_id = entry.id
#
#         # Delete the entry
#         response = logged_in_client.post(f'/delete/{entry_id}')
#
#         # Check if the entry is deleted successfully
#         assert response.status_code == 302  # Redirects to index after deletion
#         assert Entry.query.get(entry_id) is None

from flask import Flask
import unittest

from blog import db, app
from blog.models import Entry


class TestEntryDeletion(unittest.TestCase):

    def setUp(self):
        """
        Creates a new database for the unit test to use
        """
        app.config.from_object("config.TestConfig")  # Use a separate test config
        self.app = app
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        """
        Ensures that the database is emptied for the next unit test
        """
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_delete_entry(self):
        with self.app.app_context():  # Activate the app context for database operations
            # Create an entry
            entry = Entry(title='Test Title', body='Test Body', is_published=True)
            db.session.add(entry)
            db.session.commit()

            # Get the entry ID for deletion
            entry_id = entry.id

            # Delete the entry
            response = self.client.post(f'/delete/{entry_id}')

            # Check if the entry is deleted successfully
            assert response.status_code == 302  # Redirects to index after deletion
            assert Entry.query.get(entry_id) is None
