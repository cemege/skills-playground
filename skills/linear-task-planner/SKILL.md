---
name: linear-task-planner
description: Plan iOS implementation work from Linear boards, projects, or issues by fetching task details (title, description, attachments, design links, comments) via the Linear API, saving workspace context for reuse, and producing a Markdown implementation plan for developers.
---

# Linear Task Planner

Plan iOS implementation from Linear tasks with repeatable data collection and a consistent Markdown plan output.

## Quick start

1) Capture Linear context and save it for reuse.
2) Load the Linear API token from a local env file.
3) Run the skill with the issue key.
4) Fetch the issue data needed for planning.
5) Write a Markdown plan using the template.

Example invocation:

```
$linear-task-planner SKI-1
```

In this mode, use the API token flow by default and map the issue key to `--identifier`.
`--identifier` expects the Linear key format `TEAM-123` and is resolved via the team key + issue number filter.

## Capture and persist Linear context

Collect these once per workspace/board and save them for future use:

- Workspace slug or name
- Team key and/or team id
- Project id (if the board maps to a project)
- Board URL
- Default env file path
- Auth mode (`token` or `mcp`)
- Auth scheme (`raw` for personal API key or `bearer` for OAuth)
- MCP server name (if using MCP)

Save to a local config file (repo root): `.linear-task-planner.json`.
Add it to `.gitignore` to avoid committing workspace details.

Use the helper script to initialize or update it:

```bash
python3 skills/linear-task-planner/scripts/linear_fetch.py init \
  --workspace "your-workspace" \
  --team-key "ENG" \
  --team-id "team-id" \
  --project-id "project-id" \
  --board-url "https://linear.app/your-workspace/team/ENG" \
  --env ".env.local" \
  --auth-mode token \
  --auth-scheme raw
```

When starting a plan, ask the developer which auth mode they prefer:

- **API token** (default): use the script and `LINEAR_API_TOKEN` from the env file.
- **MCP**: if they already have a local MCP server for Linear, prefer it and store `authMode=mcp` + `mcpServer`.

If `authMode=mcp`, do not use `linear_fetch.py`. Instead, call the MCP server for Linear and request the same fields as the GraphQL queries in `references/issue.graphql`, `references/project.graphql`, and `references/team.graphql`.

## Load the API token

Expect `LINEAR_API_TOKEN` in a local env file (e.g., `.env.local`, `.env`).
Use `.env.local.example` as a template.

- Keep the token out of git.
- Use `--env` on commands when the env file is not `.env.local` or `.env`.
- You can pass `--env` before or after the subcommand.

## Fetch task data

Use the helper script to pull issue or project data into JSON.

Issue data (include comments and attachments):

```bash
python3 skills/linear-task-planner/scripts/linear_fetch.py issue \
  --identifier "ENG-123" \
  --env .env.local \
  --details \
  --out plans/ENG-123.json
```

If you are using OAuth tokens, set the auth scheme:

```bash
python3 skills/linear-task-planner/scripts/linear_fetch.py issue \
  --identifier "ENG-123" \
  --details \
  --auth-scheme bearer \
  --out plans/ENG-123.json
```

Project data (list issues, then pick the target issue):

```bash
python3 skills/linear-task-planner/scripts/linear_fetch.py project \
  --id "project-id" \
  --first 50 \
  --out plans/project.json
```

Team data (board view / backlog):

```bash
python3 skills/linear-task-planner/scripts/linear_fetch.py team \
  --id "team-id" \
  --first 50 \
  --out plans/team.json
```

If a query fails due to schema changes, use the custom query path and adjust fields via the GraphQL explorer:

```bash
python3 skills/linear-task-planner/scripts/linear_fetch.py custom \
  --query skills/linear-task-planner/references/issue.graphql \
  --variables '{"issueId": "..."}'
```

## Build the Markdown plan

Use the template in `references/plan-template.md`. Populate it with:

- Title, description, and acceptance criteria
- Attachments and design links (Figma, FigJam, Zeplin, etc.)
- Recent comments for updated scope or constraints
- Dependencies, risks, and open questions
- Implementation steps and testing notes
- Best-practice checks from the SwiftUI and concurrency skills

Save the plan in `plans/{issue-identifier}.md` (create `plans/` if missing).

## Required data checklist

Always attempt to collect these fields before planning:

- Issue title, description, and URL
- Labels, priority, state, due date
- Assignee and team/project context
- Attachments (screenshots, files) and design links
- Recent comments (scope changes, edge cases, UX details)

## Apply best-practice skills while planning

When you write the plan, explicitly map decisions to the existing skills:

- `swiftui-guidelines` for state management, async patterns, and view organization
- `swift-concurrency-expert` for actor isolation, Sendable, and data-race safety
- `swiftui-performance-audit` for avoiding heavy work in `body` and identity stability
- `swiftui-ui-patterns` for NavigationStack, lists/grids, sheets, and app wiring
- `swiftui-view-refactor` for consistent view structure and MV-first patterns
- `swiftui-liquid-glass` if iOS 26+ glass UI is in scope (include fallbacks)

If any of these introduce constraints or tradeoffs, capture them in the plan under “Risks & Dependencies” or “Open Questions.”

Read the source skills as needed for detailed guidance:

- `skills/swift-concurrency-expert/SKILL.md`
- `skills/swiftui-guidelines/SKILL.md`
- `skills/swiftui-liquid-glass/SKILL.md`
- `skills/swiftui-performance-audit/SKILL.md`
- `skills/swiftui-ui-patterns/SKILL.md`
- `skills/swiftui-view-refactor/SKILL.md`

## References

- `references/linear-queries.md` for query templates and field suggestions
- `references/auth.md` for API token guidance and auth-mode notes
- `references/issue.graphql`, `references/project.graphql`, `references/team.graphql` for runnable queries
- `references/plan-template.md` for the Markdown plan skeleton
- `skills/swift-concurrency-expert/SKILL.md` for concurrency best practices
- `skills/swiftui-guidelines/SKILL.md` for SwiftUI state/data flow and async patterns
- `skills/swiftui-liquid-glass/SKILL.md` for iOS 26+ glass UI guidance
- `skills/swiftui-performance-audit/SKILL.md` for performance checklists
- `skills/swiftui-ui-patterns/SKILL.md` for UI scaffolding patterns
- `skills/swiftui-view-refactor/SKILL.md` for view structure conventions
