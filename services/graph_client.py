from __future__ import annotations

import requests
from azure.identity import ClientSecretCredential

from config.settings import settings


class GraphClient:
    def __init__(self, settings_obj=None):
        self.settings = settings_obj or settings

        if not self.settings.graph_is_configured():
            raise ValueError("Microsoft Graph settings are incomplete. Check Azure credentials in the environment.")

        self.base_url = "https://graph.microsoft.com/v1.0"
        self.scope = self.settings.graph_scope
        self.credential = ClientSecretCredential(
            tenant_id=self.settings.azure_tenant_id,
            client_id=self.settings.azure_client_id,
            client_secret=self.settings.azure_client_secret,
        )

    def get_access_token(self) -> str:
        token = self.credential.get_token(self.scope)
        return token.token

    def get(self, relative_url: str):
        token = self.get_access_token()
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }
        response = requests.get(f"{self.base_url}{relative_url}", headers=headers, timeout=30)
        response.raise_for_status()
        return response.json()

    def get_recent_messages(self, top: int = 10):
        query = f"/me/messages?$top={top}&$select=subject,from,receivedDateTime,bodyPreview&$orderby=receivedDateTime desc"
        payload = self.get(query)
        return payload.get("value", [])

    def get_overdue_tasks(self, top: int = 25):
        query = f"/me/planner/tasks?$top={top}"
        payload = self.get(query)
        return payload.get("value", [])

    def list_project_signals(self):
        return {
            "messages": self.get_recent_messages(top=5),
            "tasks": self.get_overdue_tasks(top=25),
            "pending_approvals": 0,
            "last_activity_days": 0,
            "calendar_days_since_last_meeting": 0,
        }
