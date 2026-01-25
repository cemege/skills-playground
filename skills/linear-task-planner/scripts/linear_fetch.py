#!/usr/bin/env python3
import argparse
import json
import os
import re
import sys
from pathlib import Path
from typing import Optional
from urllib import request, error

DEFAULT_ENDPOINT = "https://api.linear.app/graphql"
DEFAULT_CONFIG = ".linear-task-planner.json"

QUERY_ISSUE_BY_ID = """
query IssueDetail($issueId: String!, $includeDetails: Boolean = false) {
  issue(id: $issueId) {
    id
    identifier
    title
    description
    url
    priority
    dueDate
    state {
      name
      type
    }
    labels {
      nodes {
        name
      }
    }
    assignee {
      name
      email
    }
    project {
      name
      url
    }
    updatedAt
    comments @include(if: $includeDetails) {
      nodes {
        id
        body
        user {
          name
        }
        createdAt
      }
    }
    attachments @include(if: $includeDetails) {
      nodes {
        id
        title
        url
        createdAt
      }
    }
  }
}
"""

QUERY_ISSUE_BY_IDENTIFIER = """
query IssueByIdentifier($teamKey: String!, $number: Float!, $includeDetails: Boolean = false) {
  issues(filter: { number: { eq: $number }, team: { key: { eq: $teamKey } } }) {
    nodes {
      id
      identifier
      title
      description
      url
      priority
      dueDate
      state {
        name
        type
      }
      labels {
        nodes {
          name
        }
      }
      assignee {
        name
        email
      }
      project {
        name
        url
      }
      updatedAt
      comments @include(if: $includeDetails) {
        nodes {
          id
          body
          user {
            name
          }
          createdAt
        }
      }
      attachments @include(if: $includeDetails) {
        nodes {
          id
          title
          url
          createdAt
        }
      }
    }
  }
}
"""

QUERY_PROJECT = """
query ProjectDetail($projectId: String!, $first: Int = 50) {
  project(id: $projectId) {
    id
    name
    description
    url
    state
    lead {
      name
    }
    targetDate
    updatedAt
    issues(first: $first, orderBy: updatedAt) {
      nodes {
        id
        identifier
        title
        url
        priority
        state {
          name
          type
        }
        assignee {
          name
        }
        updatedAt
      }
    }
  }
}
"""

QUERY_TEAM = """
query TeamIssues($teamId: String!, $first: Int = 50) {
  team(id: $teamId) {
    id
    name
    key
    issues(first: $first, orderBy: updatedAt) {
      nodes {
        id
        identifier
        title
        url
        priority
        state {
          name
          type
        }
        assignee {
          name
        }
        updatedAt
      }
    }
  }
}
"""


def load_env_file(path: Path) -> dict:
    env = {}
    if not path or not path.exists():
        return env
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line[len("export ") :].strip()
        if "=" not in line:
            continue
        key, value = line.split("=", 1)
        env[key.strip()] = value.strip().strip('"').strip("'")
    return env


def resolve_env_path(arg_env: str, config: dict) -> Optional[Path]:
    if arg_env:
        return Path(arg_env)
    config_env = config.get("envFile")
    if config_env:
        return Path(config_env)
    for candidate in (".env.local", ".env"):
        candidate_path = Path(candidate)
        if candidate_path.exists():
            return candidate_path
    return None


def load_config(path: Path) -> dict:
    if path.exists():
        try:
            return json.loads(path.read_text())
        except json.JSONDecodeError:
            return {}
    return {}


def write_config(path: Path, config: dict) -> None:
    path.write_text(json.dumps(config, indent=2) + "\n")


def parse_issue_identifier(identifier: str) -> tuple[str, int]:
    value = identifier.strip()
    match = re.match(r"^([A-Za-z][A-Za-z0-9_]*)-(\d+)$", value)
    if not match:
        raise ValueError(f"Invalid issue identifier '{identifier}'. Expected format TEAM-123.")
    team_key = match.group(1).upper()
    number = int(match.group(2))
    return team_key, number


def format_auth_header(token: str, scheme: Optional[str]) -> str:
    if scheme:
        scheme_value = scheme.strip().lower()
        if scheme_value in {"bearer", "oauth"}:
            if token.lower().startswith("bearer "):
                return token
            return f"Bearer {token}"
        if scheme_value in {"raw", "token"}:
            return token
    if token.lower().startswith("bearer "):
        return token
    if " " in token:
        return token
    return token


def post_graphql(
    endpoint: str,
    token: str,
    auth_scheme: Optional[str],
    query: str,
    variables: dict,
    extra_headers: dict,
) -> dict:
    payload = json.dumps({"query": query, "variables": variables}).encode("utf-8")
    req = request.Request(endpoint, data=payload, method="POST")
    req.add_header("Content-Type", "application/json")
    req.add_header("Authorization", format_auth_header(token, auth_scheme))
    for key, value in extra_headers.items():
        req.add_header(key, value)
    try:
        with request.urlopen(req) as resp:
            body = resp.read().decode("utf-8")
            return json.loads(body)
    except error.HTTPError as exc:
        error_body = exc.read().decode("utf-8") if exc.fp else ""
        raise RuntimeError(f"Request failed: HTTP {exc.code} {error_body}")


def resolve_token(args, env_data: dict) -> Optional[str]:
    if args.token:
        return args.token
    if os.environ.get("LINEAR_API_TOKEN"):
        return os.environ.get("LINEAR_API_TOKEN")
    return env_data.get("LINEAR_API_TOKEN")


def write_output(data: dict, out_path: Optional[str]) -> None:
    output = json.dumps(data, indent=2)
    if not out_path or out_path == "-":
        print(output)
        return
    path = Path(out_path)
    if path.parent and not path.parent.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(output + "\n")


def raise_on_errors(response: dict) -> None:
    errors = response.get("errors")
    if not errors:
        return
    message = "; ".join(error.get("message", "Unknown error") for error in errors)
    raise RuntimeError(f"GraphQL error: {message}")


def parse_variables(value: Optional[str]) -> dict:
    if not value:
        return {}
    if value.startswith("@"):
        raw = Path(value[1:]).read_text()
        return json.loads(raw)
    possible_path = Path(value)
    if possible_path.exists():
        return json.loads(possible_path.read_text())
    return json.loads(value)


def main() -> None:
    parser = argparse.ArgumentParser(description="Fetch Linear data for task planning.")
    parser.add_argument("--endpoint", default=DEFAULT_ENDPOINT)
    parser.add_argument("--token", help="Override LINEAR_API_TOKEN")
    parser.add_argument("--env", help="Path to env file containing LINEAR_API_TOKEN")
    parser.add_argument("--config", default=DEFAULT_CONFIG, help="Path to config JSON")
    parser.add_argument(
        "--auth-scheme",
        help="Auth scheme override: raw (personal key) or bearer (OAuth)",
    )
    parser.add_argument(
        "--public-file-urls-expire-in",
        dest="public_file_urls_expire_in",
        help="Seconds for signed attachment URLs",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    init_parser = subparsers.add_parser("init", help="Initialize or update Linear context")
    init_parser.add_argument("--env", help="Path to env file containing LINEAR_API_TOKEN")
    init_parser.add_argument("--workspace", help="Workspace slug or name")
    init_parser.add_argument("--team-id", help="Team id")
    init_parser.add_argument("--team-key", help="Team key (e.g., ENG)")
    init_parser.add_argument("--project-id", help="Project id")
    init_parser.add_argument("--project-name", help="Project name")
    init_parser.add_argument("--board-url", help="Board URL")
    init_parser.add_argument(
        "--auth-mode",
        choices=["token", "mcp"],
        help="Auth mode to use for future requests",
    )
    init_parser.add_argument(
        "--auth-scheme",
        choices=["raw", "bearer"],
        help="Auth scheme for API token mode",
    )
    init_parser.add_argument("--mcp-server", help="MCP server name (if auth-mode=mcp)")

    issue_parser = subparsers.add_parser("issue", help="Fetch issue detail")
    issue_parser.add_argument("--id", help="Issue id")
    issue_parser.add_argument("--identifier", help="Issue identifier (e.g., ENG-123)")
    issue_parser.add_argument("--env", help="Path to env file containing LINEAR_API_TOKEN")
    issue_parser.add_argument(
        "--auth-scheme",
        help="Auth scheme override: raw (personal key) or bearer (OAuth)",
    )
    issue_parser.add_argument("--details", action="store_true", help="Include comments/attachments")
    issue_parser.add_argument("--out", help="Output path (default: stdout)")

    project_parser = subparsers.add_parser("project", help="Fetch project detail and issues")
    project_parser.add_argument("--id", help="Project id (defaults to config projectId)")
    project_parser.add_argument("--env", help="Path to env file containing LINEAR_API_TOKEN")
    project_parser.add_argument(
        "--auth-scheme",
        help="Auth scheme override: raw (personal key) or bearer (OAuth)",
    )
    project_parser.add_argument("--first", type=int, default=50, help="Number of issues to fetch")
    project_parser.add_argument("--out", help="Output path (default: stdout)")

    team_parser = subparsers.add_parser("team", help="Fetch team issues")
    team_parser.add_argument("--id", help="Team id (defaults to config teamId)")
    team_parser.add_argument("--env", help="Path to env file containing LINEAR_API_TOKEN")
    team_parser.add_argument(
        "--auth-scheme",
        help="Auth scheme override: raw (personal key) or bearer (OAuth)",
    )
    team_parser.add_argument("--first", type=int, default=50, help="Number of issues to fetch")
    team_parser.add_argument("--out", help="Output path (default: stdout)")

    custom_parser = subparsers.add_parser("custom", help="Run a custom GraphQL query")
    custom_parser.add_argument("--query", required=True, help="Path to .graphql file")
    custom_parser.add_argument("--variables", help="JSON string, @file, or path")
    custom_parser.add_argument("--env", help="Path to env file containing LINEAR_API_TOKEN")
    custom_parser.add_argument(
        "--auth-scheme",
        help="Auth scheme override: raw (personal key) or bearer (OAuth)",
    )
    custom_parser.add_argument("--out", help="Output path (default: stdout)")

    args = parser.parse_args()

    config_path = Path(args.config)
    config = load_config(config_path)

    if args.command == "init":
        updates = {
            "workspace": args.workspace,
            "teamId": args.team_id,
            "teamKey": args.team_key,
            "projectId": args.project_id,
            "projectName": args.project_name,
            "boardUrl": args.board_url,
            "envFile": args.env or config.get("envFile"),
            "authMode": args.auth_mode,
            "authScheme": args.auth_scheme,
            "mcpServer": args.mcp_server,
        }
        clean_updates = {k: v for k, v in updates.items() if v}
        config.update(clean_updates)
        write_config(config_path, config)
        print(f"Saved config to {config_path}")
        return

    auth_mode = config.get("authMode") or "token"
    if auth_mode == "mcp":
        raise RuntimeError("Auth mode is set to mcp. Use MCP connectivity for this workspace.")

    env_path = resolve_env_path(args.env, config)
    env_data = load_env_file(env_path) if env_path else {}

    token = resolve_token(args, env_data)
    if not token:
        raise RuntimeError("LINEAR_API_TOKEN not found in env or args")

    extra_headers = {}
    if args.public_file_urls_expire_in:
        extra_headers["public-file-urls-expire-in"] = str(args.public_file_urls_expire_in)

    if args.command == "issue":
        if not args.id and not args.identifier:
            parser.error("issue requires --id or --identifier")
        if args.id:
            query = QUERY_ISSUE_BY_ID
            variables = {"issueId": args.id, "includeDetails": args.details}
        else:
            query = QUERY_ISSUE_BY_IDENTIFIER
            team_key, number = parse_issue_identifier(args.identifier)
            variables = {
                "teamKey": team_key,
                "number": float(number),
                "includeDetails": args.details,
            }
        auth_scheme = args.auth_scheme or config.get("authScheme")
        response = post_graphql(args.endpoint, token, auth_scheme, query, variables, extra_headers)
        raise_on_errors(response)
        if args.identifier:
            nodes = response.get("data", {}).get("issues", {}).get("nodes", [])
            if len(nodes) == 0:
                raise RuntimeError(f"No issue found for identifier {args.identifier}")
            if len(nodes) > 1:
                identifiers = ", ".join(node.get("identifier", "?") for node in nodes)
                raise RuntimeError(
                    "Multiple issues matched identifier. Use --id instead. "
                    f"Matches: {identifiers}"
                )
        write_output(response, args.out)
        return

    if args.command == "project":
        project_id = args.id or config.get("projectId")
        if not project_id:
            parser.error("project requires --id or config projectId")
        variables = {"projectId": project_id, "first": args.first}
        auth_scheme = args.auth_scheme or config.get("authScheme")
        response = post_graphql(args.endpoint, token, auth_scheme, QUERY_PROJECT, variables, extra_headers)
        raise_on_errors(response)
        write_output(response, args.out)
        return

    if args.command == "team":
        team_id = args.id or config.get("teamId")
        if not team_id:
            parser.error("team requires --id or config teamId")
        variables = {"teamId": team_id, "first": args.first}
        auth_scheme = args.auth_scheme or config.get("authScheme")
        response = post_graphql(args.endpoint, token, auth_scheme, QUERY_TEAM, variables, extra_headers)
        raise_on_errors(response)
        write_output(response, args.out)
        return

    if args.command == "custom":
        query_path = Path(args.query)
        if not query_path.exists():
            raise RuntimeError(f"Query file not found: {query_path}")
        query = query_path.read_text()
        variables = parse_variables(args.variables)
        auth_scheme = args.auth_scheme or config.get("authScheme")
        response = post_graphql(args.endpoint, token, auth_scheme, query, variables, extra_headers)
        raise_on_errors(response)
        write_output(response, args.out)
        return


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)
