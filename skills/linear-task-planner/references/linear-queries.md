# Linear GraphQL query notes

## Endpoint and headers

- Endpoint: https://api.linear.app/graphql
- Required headers:
  - Authorization: <LINEAR_API_TOKEN> (personal API key) or Bearer <ACCESS_TOKEN> (OAuth)
  - Content-Type: application/json
- Optional header for signed attachment URLs:
  - public-file-urls-expire-in: <seconds>

See `references/auth.md` for full token guidance.

## Core issue fields for planning

Prefer these fields when writing the plan:

- identifier, title, description, url
- state { name, type }
- priority, dueDate
- labels { nodes { name } }
- assignee { name, email }
- project { name, url }
- updatedAt

Note: fetching by issue key uses the team key + issue number filter (e.g., `SKI-1` → `team.key=SKI` + `number=1`).

## Extended context

- comments { nodes { body, user { name }, createdAt } }
- attachments { nodes { title, url, createdAt } }

If a field fails, remove it and re-run. Use the GraphQL explorer to validate fields for your workspace.
