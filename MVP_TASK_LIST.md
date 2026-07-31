# TempoPilot Sprint Plan

## This sprint: Graph calendar integration
- [x] Set up the Python backend scaffold
- [x] Add shared signal model for project risk inputs
- [x] Add Graph client foundation and authentication flow
- [x] Add calendar event fetch from Microsoft Graph
- [x] Add calendar inactivity to the risk engine
- [x] Add API route that builds signals and evaluates risk
- [x] Add initial tests for risk logic
- [ ] Validate the calendar signal against a real tenant
- [ ] Confirm Graph permissions and consent for calendar access
- [ ] Filter events by project context instead of generic calendar data
- [ ] Tune the PM-calendar risk thresholds
- [ ] Add error handling for Graph and AI failures
- [ ] Connect the Teams agent to the API once the backend is validated

## Next sprint priorities
- [ ] Configure Azure credentials in the local environment
- [ ] Test real Graph calendar calls against a Microsoft 365 tenant
- [ ] Normalize project-specific meeting data into the signal model
- [ ] Validate the API output with real project data

## Future signal sources to add later
- [ ] Approval delays and response latency
- [ ] Overdue tasks and unmanaged work items
- [ ] Stakeholder engagement and last activity tracking
- [ ] Email and message activity patterns
- [ ] File collaboration and shared document updates
- [ ] Project milestone drift and deadline risk

## Future platform work
- [ ] Add AI prompt refinement and stronger explanation quality
- [ ] Add Dataverse or persistent storage for risk snapshots
- [ ] Add automated follow-ups and escalation actions
- [ ] Add CI pipeline and deployment workflow
