from models.signals import build_signal
from services.risk_engine import summarize_risk


def test_risk_summary_with_high_risk_signals():
    signals = build_signal(
        project_name="Launch Campaign",
        pending_approvals=6,
        tasks=[{"id": 1}, {"id": 2}, {"id": 3}],
        last_activity_days=9,
    )

    result = summarize_risk(signals)

    assert result["project_name"] == "Launch Campaign"
    assert result["risk_level"] in {"Moderate", "High"}
    assert result["risk_score"] > 0
    assert len(result["recommended_actions"]) >= 3


def test_risk_summary_with_low_risk_signals():
    signals = build_signal(
        project_name="Routine Work",
        pending_approvals=1,
        tasks=[{"id": 1}],
        last_activity_days=2,
    )

    result = summarize_risk(signals)

    assert result["risk_level"] == "Low"
    assert result["risk_score"] < 35


def test_risk_summary_uses_calendar_inactivity_signal():
    signals = build_signal(
        project_name="Launch Campaign",
        pending_approvals=1,
        tasks=[{"id": 1}],
        last_activity_days=2,
        calendar_days_since_last_meeting=6,
    )

    result = summarize_risk(signals)

    assert result["risk_level"] in {"Moderate", "High"}
    assert any("meeting" in reason.lower() for reason in result["reasons"])
    assert result["risk_score"] >= 25
