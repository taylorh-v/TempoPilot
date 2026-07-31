# Dataverse Integration

## Purpose

Dataverse provides the structured persistence layer for TempoPilot. It stores project records, risk scores, and recommendation history so the platform can track project health over time instead of relying only on live event data.

## Why Dataverse belongs in the architecture

The backend can score a project in real time, but an operational AI system also needs durable records. Dataverse is the right place to store:

- project metadata
- project owners and stakeholders
- risk snapshots over time
- recommended actions
- actions taken or escalated
- signal summaries for reporting

## Where it fits in the codebase

The integration should live in the service layer, alongside Graph and AI services.

Recommended file layout:

```text
services/
├── graph_client.py
├── openai_service.py
├── risk_engine.py
├── dataverse_client.py
```

This keeps the responsibilities clean:

- `graph_client.py` → Microsoft Graph data collection
- `risk_engine.py` → evaluate risk from signals
- `openai_service.py` → generate AI explanation
- `dataverse_client.py` → save risk results into Dataverse

## Recommended flow

1. The API collects signals from Graph
2. The risk engine scores the project
3. The app prepares a risk record payload
4. The Dataverse service writes the record
5. Teams or the Copilot Studio agent can reference the stored risk state later

## Example record shape

```python
{
    "projectName": "Launch Campaign",
    "riskScore": 65,
    "riskLevel": "Moderate",
    "reasons": ["approval delays are growing", "no project meeting has occurred in the last 6 days"],
    "recommendedActions": ["Schedule a project coordination meeting", "Prioritize overdue work items"],
    "createdAt": "2026-07-31T00:00:00Z"
}
```

## Best implementation pattern

Add a Dataverse service that exposes a method like:

```python
save_risk_record(risk_payload: dict) -> dict
```

Then call it from the main API route after the risk has been calculated.

## Security and design notes

- use Microsoft Entra identity for authentication
- keep Dataverse access scoped and least-privileged
- avoid storing raw secret data in the record payload
- keep risk artifacts minimal and structured
- only save human-readable summaries and scores, not large unfiltered Graph dumps

## Future extension

Once the MVP is stable, Dataverse can also support:

- historical risk trend reporting
- dashboarding for project health
- audit trails for AI recommendations
- action tracking and closure history

This is the right persistence layer for the long-term TempoPilot platform.