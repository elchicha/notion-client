import pytest
import os

from dotenv import load_dotenv
from notion.client import NotionClient

load_dotenv()

notion_api = os.getenv("NOTION_API_TOKEN")


class TestNotionAuthentication:
    """Test that authentication with Notion API works"""

    @pytest.fixture
    def client(self):
        return NotionClient(api_token=os.getenv("NOTION_API_TOKEN"))

    def test_authentication_works(self, client):
        """Verify API token authenticates successfully"""
        if not os.getenv("NOTION_API_TOKEN"):
            pytest.skip("No API token in .env")

        # We'll call a simple endpoint to verify auth works
        # The /users/me endpoint would be perfect, but let's check docs
        # For now, we'll use search (which we need anyway)

        # This should succeed if auth is correct
        # This should fail with 401 if auth is wrong
        result = client.search()

        assert result is not None
        assert "results" in result

        print(f"\n✅ Authentication successful!")
        print(f"Response has {len(result['results'])} items")


class TestNotionDatabase:
    """Test database operations - following official tutorial"""

    @pytest.fixture
    def client(self):
        return NotionClient(api_token=os.getenv("NOTION_API_TOKEN"))

    @pytest.fixture
    def database_id(self):
        db_id = os.getenv("NOTION_DATABASE_ID")
        if not db_id:
            pytest.skip("No NOTION_DATABASE_ID in .env")
        return db_id

    def test_get_database(self, client, database_id):
        """
        Retrieve a database by ID
        Tutorial step: https://developers.notion.com/docs/create-a-notion-integration#step-2-share-a-database-with-your-integration
        """
        database = client.get_database(database_id)

        assert database is not None
        # assert database["object"] == "database"
        # assert database["id"] == database_id.replace("-", "")  # Notion removes dashes
        #
        # print(f"\n✅ Database retrieved!")
        # print(f"Title: {database.get('title', [{}])[0].get('plain_text', 'No title')}")
        # print(f"Properties: {list(database.get('properties', {}).keys())}")
