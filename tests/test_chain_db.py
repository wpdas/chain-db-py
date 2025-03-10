"""Tests for the ChainDB Python client."""

import pytest
import asyncio
from unittest.mock import patch, MagicMock
from chain_db import connect, Connection, ChainDB, Table, TableDoc

@pytest.mark.asyncio
async def test_connect():
    """Test connecting to ChainDB."""
    with patch('chain_db.chain_db.post') as mock_post:
        # Mock the response from the server
        mock_post.return_value = {
            'success': True,
            'data': 'test-auth-token'
        }
        
        # Create a connection
        connection = Connection(
            server="http://localhost:2818",
            database="test-db",
            user="root",
            password="1234"
        )
        
        # Connect to ChainDB
        db = await connect(connection)
        
        # Check that the connection was successful
        assert db.server == "http://localhost:2818"
        assert db.database == "test-db"
        assert db.auth == "test-auth-token"
        
        # Check that post was called with the correct arguments
        mock_post.assert_called_once_with(
            "http://localhost:2818/api/v1/database/connect",
            {
                "name": "test-db",
                "user": "root",
                "password": "1234"
            }
        )

@pytest.mark.asyncio
async def test_get_table():
    """Test getting a table from ChainDB."""
    with patch('chain_db.table.get') as mock_get:
        # Mock the response from the server
        mock_get.return_value = {
            'success': True,
            'data': {
                'greeting': 'Hello, World!',
                'doc_id': 'test-doc-id'
            }
        }
        
        # Create a ChainDB instance
        db = ChainDB()
        db.server = "http://localhost:2818"
        db.database = "test-db"
        db.auth = "test-auth-token"
        
        # Get a table
        table = await db.get_table("greeting")
        
        # Check that the table was created correctly
        assert table.name == "greeting"
        assert table.db == db
        assert table.currentDoc == {
            'greeting': 'Hello, World!',
            'doc_id': 'test-doc-id'
        }
        
        # Check that get was called with the correct arguments
        mock_get.assert_called_once_with(
            "http://localhost:2818/api/v1/table/greeting",
            "test-auth-token"
        )

@pytest.mark.asyncio
async def test_persist():
    """Test persisting data to ChainDB."""
    with patch('chain_db.table.post') as mock_post:
        # Mock the response from the server
        mock_post.return_value = {
            'success': True,
            'data': {
                'greeting': 'Hello, World!',
                'doc_id': 'test-doc-id'
            }
        }
        
        # Create a ChainDB instance
        db = ChainDB()
        db.server = "http://localhost:2818"
        db.database = "test-db"
        db.auth = "test-auth-token"
        
        # Create a table
        table = Table("greeting", db)
        table.currentDoc = {
            'greeting': 'Hello, World!'
        }
        
        # Persist data
        result = await table.persist()
        
        # Check that the result is correct
        assert result == {
            'greeting': 'Hello, World!',
            'doc_id': 'test-doc-id'
        }
        
        # Check that post was called with the correct arguments
        mock_post.assert_called_once_with(
            "http://localhost:2818/api/v1/table/greeting/persist",
            {
                "data": {
                    'greeting': 'Hello, World!'
                }
            },
            "test-auth-token"
        )

@pytest.mark.asyncio
async def test_get_doc():
    """Test getting a document from ChainDB."""
    with patch('chain_db.table.get') as mock_get:
        # Mock the response from the server
        mock_get.return_value = {
            'success': True,
            'data': {
                'greeting': 'Hello, World!',
                'doc_id': 'test-doc-id'
            }
        }
        
        # Create a ChainDB instance
        db = ChainDB()
        db.server = "http://localhost:2818"
        db.database = "test-db"
        db.auth = "test-auth-token"
        
        # Create a table
        table = Table("greeting", db)
        
        # Get a document
        doc = await table.get_doc("test-doc-id")
        
        # Check that the document was created correctly
        assert doc.table_name == "greeting"
        assert doc.doc_id == "test-doc-id"
        assert doc.doc == {
            'greeting': 'Hello, World!',
            'doc_id': 'test-doc-id'
        }
        
        # Check that get was called with the correct arguments
        mock_get.assert_called_once_with(
            "http://localhost:2818/api/v1/table/greeting/doc/test-doc-id",
            "test-auth-token"
        )
