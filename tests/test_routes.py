from flask import url_for
from blog import app
import pytest
from unittest.mock import patch, MagicMock
from blog.models import Entry
from blog.routes import delete_entry
from flask import Flask


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_homepage(client):
    response = client.get('/')
    assert response.status_code == 200


def test_login(client):
    response = client.get('/login/')
    assert response.status_code == 200


def test_edit_or_create_entry_for_logged_in_user(client):
    with client.session_transaction() as session:
        session['logged_in'] = True

    response = client.get('/post/')
    assert response.status_code == 200


def test_edit_or_create_entry_for_logged_out_user(client):
    with client.session_transaction() as session:
        session['logged_in'] = False

    response = client.get('/post/')
    assert response.status_code == 302  # Redirects to /login/

    # You can continue testing the POST method, form submission, etc.


def test_logout(client):
    # Assuming a logged-in user for this test
    with client.session_transaction() as session:
        session['logged_in'] = True

    response = client.post('/logout/')
    assert response.status_code == 302  # Redirects to index after logout
    # Add more assertions if needed


def test_list_drafts_for_logged_in_user(client):
    with client.session_transaction() as session:
        session['logged_in'] = True

    response = client.get('/drafts/')
    assert response.status_code == 200
    # Add assertions to test draft listing, etc.


def test_list_drafts_for_logged_out_user(client):
    with client.session_transaction() as session:
        session['logged_in'] = False

    response = client.get('/drafts/')
    assert response.status_code == 302  # Redirects to /login/
    # Add assertions to test draft listing, etc.

# def test_delete_entry(client):
#     # Assuming a logged-in user for this test
#     with client.session_transaction() as session:
#         session['logged_in'] = True
#
#     # Assuming an entry ID exists for testing deletion
#     response = client.post('/delete/1', follow_redirects=True)
#     assert response.status_code == 200
#     # Add assertions to test entry deletion, flash messages, etc.

# def test_delete_entry(client):
#     # Assuming a logged-in user for this test
#     with client.session_transaction() as session:
#         session['logged_in'] = True
#
#     with app.app_context():  # Set up the application context
#         # Assuming an entry ID exists for testing deletion
#         with patch('blog.models.Entry.query') as mock_query:
#             mock_entry = mock_query.get_or_404.return_value
#             response = client.post('/delete/11', follow_redirects=True)
#             assert response.status_code == 200
#             # Add assertions to test entry deletion, flash messages, etc.


# def test_delete_entry(monkeypatch):
#     app = Flask(__name__)  # Create a Flask app instance
#     app.config['TESTING'] = True  # Set the app to testing mode
#
#     with client.session_transaction() as session:
#         session['logged_in'] = True
#
#     with app.app_context():  # Establish application context
#         # Mocking the db.session.delete and db.session.commit methods
#         mock_delete = MagicMock()
#         mock_commit = MagicMock()
#         monkeypatch.setattr('blog.routes.db.session.delete', mock_delete)
#         monkeypatch.setattr('blog.routes.db.session.commit', mock_commit)
#
#         # Simulate an entry ID for deletion
#         entry_id = 1  # Replace this with an existing entry ID
#
#         with app.test_request_context():  # Create a request context
#             # Call the delete_entry route function
#             delete_entry(entry_id)
