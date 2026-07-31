# TempoPilot MVP Task List

## Status legend
- [x] Done
- [ ] Planned / not started
- [ ] In progress

## Completed during initial MVP setup
- [x] Create the project workspace structure for the Python API MVP
- [x] Add base dependencies in `requirements.txt`
- [x] Add example environment configuration in `.env.example`
- [x] Create centralized app settings in `config/settings.py`
- [x] Build a Microsoft Graph client scaffold in `services/graph_client.py`
- [x] Add a FastAPI app entry point in `app.py`
- [x] Add a risk-scoring engine in `services/risk_engine.py`
- [x] Add calendar inactivity risk logic for project manager coordination gaps
- [x] Add Azure OpenAI integration scaffold in `services/openai_service.py`
- [x] Add initial tests for risk logic in `tests/test_risk_engine.py`
- [x] Record the project task plan in this file

## MVP backend tasks to complete next
- [ ] Configure local environment variables with real Azure credentials
- [ ] Validate Microsoft Graph permissions and consent for the app registration
- [ ] Test Graph calls against a real tenant or sample data
- [ ] Replace placeholder Graph logic with real project-based filtering
- [ ] Add project signal normalization for approvals, tasks, messages, and engagement
- [ ] Add structured risk scoring rules based on project health metrics
- [ ] Add actual AI prompt templates for root-cause analysis and recommendations
- [ ] Security-review the app for least-privilege permissions and secret handling
- [ ] Add health checks and operational logging for production readiness
- [ ] Add API authentication or Teams-integrated access control
- [ ] Add data persistence for risk snapshots in Dataverse or a database
- [ ] Add endpoint(s) for a single project, multiple projects, and action summaries
- [ ] Add retry handling, timeouts, and error responses for Graph/OpenAI calls
- [ ] Add CI pipeline with linting and testing via GitHub Actions
- [ ] Create a simple sample payload and demo script for testing the API

## Teams + Copilot Studio integration tasks
- [ ] Confirm the agent already started is connected to your Microsoft 365 tenant
- [ ] Define the Teams user flow for asking about project risk
- [ ] Design how the Teams agent calls the backend API
- [ ] Add a fallback for cases where Graph data is unavailable
- [ ] Decide whether automation is handled inside Teams, Power Automate, or both

## Production readiness checklist
- [ ] Use Microsoft Entra ID and proper app registration setup
- [ ] Implement environment separation for dev/test/prod
- [ ] Add monitoring, tracing, and alerting
- [ ] Define access policies and governance for AI-generated actions
- [ ] Confirm what actions the system is allowed to trigger automatically
- [ ] Add human approval checks for high-impact automation

## Recommended next milestone
- [ ] Complete the backend MVP with real Graph + AI integration
- [ ] Test via Swagger or local API requests
- [ ] Connect the Teams side to the API
- [ ] Validate end-to-end project risk output
- [ ] Move to production-ready hardening
