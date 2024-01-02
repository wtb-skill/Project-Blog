from flask import url_for
from blog import app, db, models
from config import TestConfig
import pytest
from unittest.mock import patch, MagicMock, Mock
from blog.models import Entry
from blog.routes import delete_entry
from flask import Flask


# @pytest.fixture
# def client():
#     app.config['TESTING'] = True
#     with app.test_client() as client:
#         yield client


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


@pytest.fixture(scope='function')
def app_client():
    app.config.from_object(TestConfig)
    app.testing = True
    client = app.test_client()

    with app.app_context():
        db.create_all()

    yield client

    with app.app_context():
        db.drop_all()


def test_login_access(logged_out_client, app_client):
    response = logged_out_client.get('/login/')
    assert response.status_code == 200


def test_logout_access(logged_in_client, app_client):
    response = logged_in_client.post('/logout/')

    assert response.status_code == 302
    assert response.headers['Location'] == url_for('index')


def test_homepage_access(logged_in_client, logged_out_client, app_client):
    response_logged_in = logged_in_client.get('/')
    response_logged_out = logged_out_client.get('/')

    assert response_logged_in.status_code == 200
    assert response_logged_out.status_code == 200


def test_entry_editing_and_creation_access(logged_in_client, logged_out_client, app_client):
    url = '/post/'
    response_logged_in = logged_in_client.get(url)
    response_logged_out = logged_out_client.get(url)

    assert response_logged_in.status_code == 200
    assert response_logged_out.status_code == 302
    assert response_logged_out.headers['Location'] == url_for('login', next=url)


def test_list_drafts_access(logged_in_client, logged_out_client, app_client):
    url = '/drafts/'
    response_logged_in = logged_in_client.get(url)
    response_logged_out = logged_out_client.get(url)

    assert response_logged_in.status_code == 200
    assert response_logged_out.status_code == 302
    assert response_logged_out.headers['Location'] == url_for('login', next=url)


def test_delete_entry(logged_in_client, app_client):
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



