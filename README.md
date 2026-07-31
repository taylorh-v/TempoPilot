# TempoPilot

AI-powered coordination intelligence for Microsoft 365.

TempoPilot is a Microsoft 365 project-risk agent that detects coordination issues early by analyzing collaboration signals across Teams, email, tasks, and calendar activity. It identifies risks such as delayed approvals, missed commitments, stakeholder disengagement, and declining project momentum, then explains the likely cause and recommends action.

## Project goal

Turn Microsoft 365 activity into early warning indicators for project health.

## Architecture

```text
Microsoft Teams
   │
   ▼
Copilot Studio
   │
   ├─ Azure OpenAI
   ├─ Microsoft Graph
   ├─ Azure AI Search
   ├─ Dataverse
   └─ Power Automate
```

This repository contains the initial Python backend MVP for the intelligence layer.

## Current repo structure

```text
TempoPilot/
├── app.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
├── MVP_TASK_LIST.md
├── RISK_ENGINE_README.md
├── config/
│   └── settings.py
├── models/
│   └── signals.py
├── services/
│   ├── graph_client.py
│   ├── risk_engine.py
│   └── openai_service.py
├── tests/
│   └── test_risk_engine.py
└── .venv/
```

## Core stack

- Microsoft Teams
- Copilot Studio
- Microsoft Graph API
- Azure OpenAI
- Azure AI Search
- Dataverse
- Power Automate
- Python + FastAPI

## MVP features

- Microsoft Graph client scaffold
- signal normalization model
- project risk scoring engine
- calendar inactivity signal for project manager coordination gaps
- Azure OpenAI integration hook
- basic automated tests for risk logic

## Current risk signal

The first implemented coordination signal is calendar inactivity.

If a project manager has not met with the team in 6+ days, the system raises the project risk score and flags coordination drift as a reason for concern.

## Quick start

1. Create a Python environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Copy the example environment file and add your Azure values:

```bash
copy .env.example .env
```

4. Start the API:

```bash
uvicorn app:app --reload
```

5. Call the risk endpoint:

```text
GET /api/project-risk
```

## Current status

This is an MVP backend foundation for the full TempoPilot system. The next steps are real Microsoft Graph data integration, tenant-specific configuration, and connection to the Teams/Copilot experience.

## Notes

- Secrets are not committed to source control.
- The repo includes a .gitignore for local environment files.
- Runtime validation is still pending real environment setup for Azure and Python dependencies.

> TempoPilot turns Microsoft 365 collaboration signals into proactive project risk intelligence.