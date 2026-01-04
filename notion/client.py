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
