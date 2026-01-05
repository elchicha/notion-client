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
        Retrieve a database and explore its data sources
        New API: A database can have multiple data sources
        """
        database = client.get_database(database_id)

        assert database is not None
        assert database["object"] == "database"

        print(f"\n✅ Database retrieved!")
        print(f"Database ID: {database['id']}")

        # New API: databases have data_sources array
        data_sources = database.get("data_sources", [])
        print(f"\nData sources: {len(data_sources)}")

        for i, ds in enumerate(data_sources):
            print(f"\n  Data Source {i+1}:")
            print(f"    ID: {ds.get('id')}")
            print(f"    Name: {ds.get('name', 'Unnamed')}")
            print(f"    Type: {ds.get('type')}")

    def test_query_database_proper_flow(self, client, database_id):
        """
        Proper flow: Get database → Extract data source ID → Query data source
        """
        # Step 1: Get database
        database = client.get_database(database_id)

        # Step 2: Extract data source ID
        data_sources = database.get("data_sources", [])
        assert len(data_sources) > 0, "Database has no data sources"

        data_source_id = data_sources[0]["id"]
        print(f"\n📊 Using data source: {data_source_id}")

        # Step 3: Query the data source
        results = client.query_data_source(data_source_id)

        assert results is not None
        assert "results" in results

        print(f"✅ Found {len(results['results'])} items")

        if results["results"]:
            first = results["results"][0]
            print(
                f"\nFirst item properties: {list(first.get('properties', {}).keys())}"
            )

    def test_query_database_convenience_method(self, client, database_id):
        """Test the convenience method that handles data source lookup"""
        results = client.query_database(database_id)

        assert results is not None
        assert "results" in results

        print(f"\n✅ Convenience method works!")
        print(f"Found {len(results['results'])} items")
