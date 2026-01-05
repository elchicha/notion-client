from typing import Any, Dict, Optional

import requests


class NotionClient:

    def __init__(self, api_token: Optional[str] = None):
        """Initialize Notion client"""
        if api_token is None:
            raise ValueError("API token is required")

        self.api_token = api_token
        self.base_url = "https://api.notion.com/v1"
        self.notion_version = "2025-09-03"

    def _get_headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self.api_token}",
            "Notion-Version": "2025-09-03",  # Latest version
            "Content-Type": "application/json",
        }

    def search(self, query: str = "") -> Dict[str, Any]:
        """
        Search for pages and databases

        Args:
            query: Search query (optional - empty returns all accessible items)

        Returns:
            Search results
        """
        url = f"{self.base_url}/search"

        body = {}
        if query:
            body["query"] = query

        response = requests.post(url, headers=self._get_headers(), json=body)
        response.raise_for_status()

        return response.json()

    def get_database(self, database_id: str) -> Dict[str, Any]:
        """
        Retrieve a database by ID

        Args:
            database_id: The database ID

        Returns:
            Database object
        """
        url = f"{self.base_url}/databases/{database_id}"
        response = requests.get(url, headers=self._get_headers())
        response.raise_for_status()

        return response.json()

    def query_database(
        self, database_id: str, filter_params: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Convenience method: Query a database's primary data source

        This wraps the proper flow:
        1. Get database
        2. Find primary data source
        3. Query it

        Args:
            database_id: The database ID
            filter_params: Optional filters/sorts

        Returns:
            Query results
        """
        # Get the primary data source ID
        data_source_id = self.get_primary_data_source_id(database_id)

        # Query it
        return self.query_data_source(data_source_id, filter_params)

    def query_data_source(
        self, data_source_id: str, filter_params: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Query a data source to get its pages/items

        Args:
            data_source_id: The data source ID
            filter_params: Optional filters, sorts, pagination

        Returns:
            Query results with pages/items
        """
        url = f"{self.base_url}/data_sources/{data_source_id}/query"

        body = filter_params or {}

        response = requests.post(url, headers=self._get_headers(), json=body)
        response.raise_for_status()

        return response.json()

    def get_database_data_sources(self, database_id: str) -> list:
        """
        Get data source IDs for a database

        In the new API, databases can have multiple data sources.
        This helper extracts them from the database object.

        Args:
            database_id: The database ID

        Returns:
            List of data source objects with IDs
        """
        database = self.get_database(database_id)
        return database.get("data_sources", [])

    def get_primary_data_source_id(self, database_id: str) -> str:
        """
        Get the primary (first) data source ID for a database

        Most databases have just one data source.

        Args:
            database_id: The database ID

        Returns:
            The primary data source ID
        """
        data_sources = self.get_database_data_sources(database_id)

        if not data_sources:
            raise ValueError(f"No data sources found for database {database_id}")

        return data_sources[0]["id"]
