DEFAULT_SIGNAL = {
    "project_name": "Sample Project",
    "pending_approvals": 0,
    "tasks": [],
    "last_activity_days": 0,
    "calendar_days_since_last_meeting": 0,
}


def build_signal(**overrides):
    signal = DEFAULT_SIGNAL.copy()
    signal["tasks"] = list(signal["tasks"])
    signal.update(overrides)
    return signal
