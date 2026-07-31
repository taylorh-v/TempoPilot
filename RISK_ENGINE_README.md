# Risk Engine README

## Purpose

The risk engine is the core decision-making component in TempoPilot. It evaluates project signals gathered from Microsoft 365 activity and converts them into a simple, explainable risk score.

Its job is to answer two questions:

1. Is the project under coordination risk?
2. Why is it at risk, and what should be done next?

The current implementation is intentionally lightweight so it is easy to understand and extend as the platform matures.

---

## File location

- [services/risk_engine.py](services/risk_engine.py)

## Main function

```python
summarize_risk(signals: dict) -> dict
```

This function accepts a dictionary of project signals and returns a structured risk summary.

---

## Inputs

The engine expects a dictionary that includes values like:

```python
{
    "project_name": "Launch Campaign",
    "pending_approvals": 6,
    "tasks": [{"id": 1}, {"id": 2}, {"id": 3}],
    "last_activity_days": 9,
}
```

### Current signals used

- `project_name`: human-readable project label
- `pending_approvals`: number of approval items awaiting action
- `tasks`: list of project tasks, usually derived from Microsoft Graph or planning data
- `last_activity_days`: number of days since meaningful team activity or stakeholder response

These are placeholders for the richer Microsoft Graph data we will integrate later.

---

## Logic

The engine does the following:

1. Reads the project name
2. Counts approval delay severity
3. Counts overdue or unresolved task volume
4. Detects inactivity by checking how old the most recent activity is
5. Adds weighted risk points for each concern
6. Classifies the result as Low, Moderate, or High
7. Returns a structured summary with reasons and recommended actions

### Current scoring rules

```python
if approval_delay_days >= 5:
    score += 30

if overdue_tasks >= 2:
    score += 25

if last_activity_days >= 7:
    score += 25
```

This means the engine is currently tuned to detect the following patterns:

- approval bottlenecks
- overdue work items
- stakeholder or team inactivity

The total score is capped at 100 to keep the output stable.

---

## Risk levels

```python
if score < 35:
    level = "Low"
elif score < 70:
    level = "Moderate"
else:
    level = "High"
```

### Interpretation

- Low: No major coordination risk detected
- Moderate: Some risk signals exist but are not severe yet
- High: Multiple risk indicators suggest project momentum is weakening

---

## Return structure

The engine returns a dictionary in this format:

```python
{
    "project_name": "Launch Campaign",
    "risk_score": 80,
    "risk_level": "High",
    "reasons": [
        "approval delays are growing",
        "multiple overdue tasks are unresolved",
        "stakeholder engagement has dropped"
    ],
    "recommended_actions": [
        "Review outstanding approvals with the project owner",
        "Prioritize overdue work items",
        "Reach out to inactive stakeholders"
    ]
}
```

This structure is designed to support:

- UI display in Teams
- API responses for downstream services
- AI-generated explanations based on the risk summary
- downstream workflow automation

---

## Why this implementation matters

The risk engine is intentionally explainable. Instead of simply returning a single score, it exposes:

- the score
- the level
- the reason list
- suggested actions

This makes it useful both for:

- end users who want understandable insight
- AI modules that need evidence before making recommendations

This supports TempoPilot’s core mission: proactive project intelligence based on real coordination signals.

---

## Extension points

This is the first version of the engine, and it is designed to be expanded. In future versions, it can incorporate:

- response latency across Teams and email
- stakeholder engagement trends over time
- task priority and dependency chains
- project milestone slippage
- approval turnaround metrics
- AI-generated root-cause explanations

Those upgrades can be integrated by adding new signal fields and weighted rules without redesigning the base structure.

---

## Example usage

```python
from services.risk_engine import summarize_risk

signals = {
    "project_name": "Launch Campaign",
    "pending_approvals": 6,
    "tasks": [{"id": 1}, {"id": 2}, {"id": 3}],
    "last_activity_days": 9,
}

result = summarize_risk(signals)
print(result)
```

---

## Notes

This file is intentionally simple and not yet connected to full Microsoft Graph data. The goal of the current version is to establish the risk model logic before integrating live organizational signals.

As the project grows, we will replace the placeholder signal fields with real Graph-derived project health indicators and increase the sophistication of the scoring model.
