from flask import url_for
from blog import app, db, models
import pytest
from unittest.mock import patch, MagicMock, Mock
from blog.models import Entry
from blog.routes import delete_entry
from flask import Flask


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def logged_in_client():
    with app.test_client() as client:
        with client.session_transaction() as session:
            session['logged_in'] = True
        yield client


@pytest.fixture
def logged_out_client():
    with app.test_client() as client:
        with client.session_transaction() as session:
            session['logged_in'] = False
        yield client


def test_login_access(logged_out_client):
    response = logged_out_client.get('/login/')
    assert response.status_code == 200


def test_logout_access(logged_in_client):
    response = logged_in_client.post('/logout/')

    assert response.status_code == 302
    assert response.headers['Location'] == url_for('index')


def test_homepage_access(logged_in_client, logged_out_client):
    response_logged_in = logged_in_client.get('/')
    response_logged_out = logged_out_client.get('/')

    assert response_logged_in.status_code == 200
    assert response_logged_out.status_code == 200


def test_entry_editing_and_creation_access(logged_in_client, logged_out_client):
    url = '/post/'
    response_logged_in = logged_in_client.get(url)
    response_logged_out = logged_out_client.get(url)

    assert response_logged_in.status_code == 200
    assert response_logged_out.status_code == 302
    assert response_logged_out.headers['Location'] == url_for('login', next=url)


def test_list_drafts_access(logged_in_client, logged_out_client):
    url = '/drafts/'
    response_logged_in = logged_in_client.get(url)
    response_logged_out = logged_out_client.get(url)

    assert response_logged_in.status_code == 200
    assert response_logged_out.status_code == 302
    assert response_logged_out.headers['Location'] == url_for('login', next=url)


# WORKS
def test_delete_existing_entry(logged_in_client):
    with app.app_context():  # Activate the app context for database operations
        # Create an entry
        entry = Entry(title='Test Title', body='Test Body', is_published=True)
        db.session.add(entry)
        db.session.commit()

        # Get the entry ID for deletion
        entry_id = entry.id

        # Delete the entry
        response = logged_in_client.post(f'/delete/{entry_id}')

        # Check if the entry is deleted successfully
        assert response.status_code == 302  # Redirects to index after deletion
        assert Entry.query.get(entry_id) is None


# DOESNT WORK
# def test_delete_entry_with_mocked_db(logged_in_client, monkeypatch):
#     with app.app_context():
#         # Create a mock entry
#         entry = Entry(id=1, title='Test Title', body='Test Body', is_published=True)
#
#         # Mocking the database functions
#         mock_get_or_404 = Mock(return_value=entry)
#         mock_delete = Mock()
#         mock_commit = Mock()
#
#         # Patching the actual functions with mocks
#         monkeypatch.setattr('blog.routes.Entry.query.get_or_404', mock_get_or_404)
#         monkeypatch.setattr('blog.routes.db.session.delete', mock_delete)
#         monkeypatch.setattr('blog.routes.db.session.commit', mock_commit)
#
#         # Make the request to delete the entry
#         response = logged_in_client.post('/delete/1')
#
#         # Assertions
#         mock_get_or_404.assert_called_once_with(1)
#         mock_delete.assert_called_once_with(entry)
#         mock_commit.assert_called_once()
#
#         assert response.status_code == 302  # Check if it redirects
#         assert response.headers['Location'] == url_for('index')  # Check if it redirects to index
#

# def test_delete_entry_with_mocked_db(logged_in_client, monkeypatch):
#     with app.app_context():
#         # Test the route without mocking database functions
#         # response = logged_in_client.post('/delete/11')
#         # assert response.status_code == 302  # Check if it redirects
#         # assert response.headers['Location'] == url_for('index')  # Check if it redirects to index
#
#         # Create a mock entry
#         entry = Entry(id=1, title='Test Title', body='Test Body', is_published=True)
#
#         # Mocking the database functions
#         mock_get_or_404 = Mock(return_value=entry)
#         mock_delete = Mock()
#         mock_commit = Mock()
#
#         # Patching the actual functions with mocks
#         print("Before patching:", Entry.query.get_or_404)  # Print the original function
#         monkeypatch.setattr('blog.routes.Entry.query.get_or_404', mock_get_or_404)
#         print("After patching:", Entry.query.get_or_404)  # Print the patched function
#
#         monkeypatch.setattr('blog.routes.db.session.delete', mock_delete)
#         monkeypatch.setattr('blog.routes.db.session.commit', mock_commit)
#
#         # Check if entry with ID 1 exists after mocked scenario
#         entry_exists = Entry.query.get_or_404(1) is not None
#         print(f"Entry with ID 1 exists: {entry_exists}")
#
#         # Make the request to delete the entry
#         response = logged_in_client.post('/delete/1')
#
#         # Assertions
#         assert mock_get_or_404.called_once_with(1)
#         assert mock_delete.called_once_with(entry)
#         assert mock_commit.called_once()
#
#         assert response.status_code == 302  # Check if it redirects
#         assert response.headers['Location'] == url_for('index')  # Check if it redirects to index

