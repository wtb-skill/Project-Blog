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

    assert response.status_code == 302  # Redirects to index after logout


def test_homepage_access(logged_in_client, logged_out_client):
    response_logged_in = logged_in_client.get('/')
    response_logged_out = logged_out_client.get('/')

    assert response_logged_in.status_code == 200
    assert response_logged_out.status_code == 200


def test_entry_editing_and_creation_access(logged_in_client, logged_out_client):
    response_logged_in = logged_in_client.get('/post/')
    response_logged_out = logged_out_client.get('/post/')

    assert response_logged_in.status_code == 200
    assert response_logged_out.status_code == 302  # Redirects to /login/


def test_list_drafts_access(logged_in_client, logged_out_client):
    response_logged_in = logged_in_client.get('/drafts/')
    response_logged_out = logged_out_client.get('/drafts/')

    assert response_logged_in.status_code == 200
    assert response_logged_out.status_code == 302  # Redirects to /login/

