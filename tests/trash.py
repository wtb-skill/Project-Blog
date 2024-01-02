# DOESNT WORK
# mock
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
from flask import url_for
from blog import app, db, models
from config import TestConfig
import pytest
from unittest.mock import patch, MagicMock, Mock
from blog.models import Entry
from blog.routes import delete_entry
from flask import Flask


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
