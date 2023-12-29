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


def test_logout(client):
    # Assuming a logged-in user for this test
    with client.session_transaction() as session:
        session['logged_in'] = True

    response = client.post('/logout/')
    assert response.status_code == 302  # Redirects to index after logout


def test_list_drafts_for_logged_in_user(client):
    with client.session_transaction() as session:
        session['logged_in'] = True

    response = client.get('/drafts/')
    assert response.status_code == 200


def test_list_drafts_for_logged_out_user(client):
    with client.session_transaction() as session:
        session['logged_in'] = False

    response = client.get('/drafts/')
    assert response.status_code == 302  # Redirects to /login/
