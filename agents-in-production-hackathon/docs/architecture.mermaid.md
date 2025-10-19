```mermaid
flowchart LR
  G[Gmail]-->R[Composio Tool Router]
  S[Slack]-->R
  Sh[Google Sheets]-->R
  T[Trello/Notion]-->R
  D[Drive]-->R
  R-->P[Planner Agent]
  P-->E[Execution Agent]
  E-->U[Slack/Trello/Gmail]
  E-->C[Compliance Log (Sheets)]
  E-->O[Ops Dashboard]
  E-->Obs[Observability]
``` 
