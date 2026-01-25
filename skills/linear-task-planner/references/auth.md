# Linear authentication guide

## Personal API key (recommended for local scripts)

1. In Linear, open **Settings → Account → Security & Access**.
2. Use **Personal API keys** to create a key.
3. Store the key in your env file as `LINEAR_API_TOKEN`.

For personal scripts, Linear expects `Authorization: <API_KEY>`.

Set `authScheme=raw` in `.linear-task-planner.json` (default).

## OAuth tokens (if building a shared app)

If you are building a shared integration, use OAuth and send the token as:

`Authorization: Bearer <ACCESS_TOKEN>`

Set `authScheme=bearer` in `.linear-task-planner.json` or pass `--auth-scheme bearer`.

## File attachments

Attachments are stored on Linear's file storage. You can either:

- Pass the same `Authorization` header when downloading `uploads.linear.app` files, or
- Request signed URLs by setting `public-file-urls-expire-in` in the GraphQL request headers.

## MCP option

Linear provides an official MCP server that lets compatible AI clients access Linear data securely. If your team already uses MCP, prefer that mode to avoid manual token handling. Store `authMode=mcp` and the MCP server name in `.linear-task-planner.json`.
