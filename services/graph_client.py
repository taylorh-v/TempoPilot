from __future__ import annotations

from datetime import datetime, timedelta, timezone

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

    def get_calendar_events(self, days_back: int = 30, top: int = 20):
        now = datetime.now(timezone.utc)
        start = (now - timedelta(days=days_back)).isoformat()
        end = (now + timedelta(days=30)).isoformat()
        query = (
            f"/me/calendar/calendarView?startDateTime={start}&endDateTime={end}"
            f"&$select=subject,start,end,organizer,attendees&$top={top}&$orderby=start/dateTime desc"
        )
        payload = self.get(query)
        return payload.get("value", [])

    def get_calendar_signal(self, project_name: str = "Sample Project", days_back: int = 120):
        events = self.get_calendar_events(days_back=days_back, top=25)
        project_name_lower = project_name.lower().strip()

        relevant_events = []
        for event in events:
            subject = (event.get("subject") or "").lower()
            if project_name_lower in subject:
                relevant_events.append(event)

        if not relevant_events:
            relevant_events = events

        if not relevant_events:
            return {
                "calendar_days_since_last_meeting": 0,
                "last_meeting_date": None,
                "last_meeting_subject": None,
            }

        latest_event = max(relevant_events, key=lambda event: event.get("start", {}).get("dateTime", "1970-01-01T00:00:00Z"))
        raw_start = latest_event.get("start", {}).get("dateTime")
        last_meeting_subject = latest_event.get("subject")

        if not raw_start:
            return {
                "calendar_days_since_last_meeting": 0,
                "last_meeting_date": None,
                "last_meeting_subject": last_meeting_subject,
            }

        try:
            meeting_time = datetime.fromisoformat(raw_start.replace("Z", "+00:00"))
        except ValueError:
            meeting_time = datetime.now(timezone.utc)

        now = datetime.now(timezone.utc)
        delta_days = max(0, (now - meeting_time.astimezone(timezone.utc)).days)

        return {
            "calendar_days_since_last_meeting": delta_days,
            "last_meeting_date": raw_start,
            "last_meeting_subject": last_meeting_subject,
        }

    def list_project_signals(self, project_name: str = "Sample Project"):
        calendar_signal = self.get_calendar_signal(project_name=project_name)
        return {
            "messages": self.get_recent_messages(top=5),
            "tasks": self.get_overdue_tasks(top=25),
            "pending_approvals": 0,
            "last_activity_days": 0,
            "calendar_days_since_last_meeting": calendar_signal["calendar_days_since_last_meeting"],
            "last_meeting_date": calendar_signal["last_meeting_date"],
            "last_meeting_subject": calendar_signal["last_meeting_subject"],
        }
