from __future__ import annotations

from models.signals import DEFAULT_SIGNAL


def _normalize_signal(signals: dict) -> dict:
    signal = {**DEFAULT_SIGNAL, **signals}
    signal["tasks"] = list(signals.get("tasks", DEFAULT_SIGNAL["tasks"]))
    return signal


def _determine_risk_level(score: int) -> str:
    if score < 35:
        return "Low"
    if score < 70:
        return "Moderate"
    return "High"


def summarize_risk(signals: dict) -> dict:
    signal = _normalize_signal(signals)

    project_name = signal.get("project_name", "Sample Project")
    approval_delay_days = signal.get("pending_approvals", 0)
    overdue_tasks = len(signal.get("tasks", []))
    last_activity_days = signal.get("last_activity_days", 0)
    calendar_days_since_last_meeting = signal.get("calendar_days_since_last_meeting", 0)

    score = 0
    reasons = []

    if approval_delay_days >= 5:
        score += 30
        reasons.append("approval delays are growing")

    if overdue_tasks >= 2:
        score += 25
        reasons.append("multiple overdue tasks are unresolved")

    if last_activity_days >= 7:
        score += 25
        reasons.append("stakeholder engagement has dropped")

    if calendar_days_since_last_meeting >= 6:
        score += 25
        reasons.append("no project meeting has occurred in the last 6 days, indicating coordination risk")
    elif calendar_days_since_last_meeting >= 3:
        score += 10
        reasons.append("project coordination is slowing down and the team has not met recently")

    risk_level = _determine_risk_level(score)

    return {
        "project_name": project_name,
        "risk_score": min(score, 100),
        "risk_level": risk_level,
        "reasons": reasons or ["limited project signals detected"],
        "recommended_actions": [
            "Review outstanding approvals with the project owner",
            "Prioritize overdue work items",
            "Reach out to inactive stakeholders",
            "Schedule a project coordination meeting to re-establish momentum",
        ],
    }
