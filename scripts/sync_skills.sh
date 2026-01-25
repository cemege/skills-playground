#!/usr/bin/env bash
set -euo pipefail

root_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
codex_skills="${root_dir}/.codex/skills"
repo_skills="${root_dir}/skills"
claude_skills="${root_dir}/.claude/skills"
force_sync="false"

if [ "${1:-}" = "--force" ]; then
  force_sync="true"
  shift
fi

mkdir -p "${codex_skills}" "${claude_skills}"

if [ ! -d "${codex_skills}" ] || [ -z "$(ls -A "${codex_skills}")" ]; then
  echo "Error: ${codex_skills} is empty. Populate it before syncing." >&2
  exit 1
fi

diff_found="false"

repo_diff="$(rsync -a --delete --dry-run --itemize-changes --exclude '.DS_Store' "${codex_skills}/" "${repo_skills}/" | sed '/^$/d')"
if [ -n "${repo_diff}" ]; then
  diff_found="true"
  echo "Diff: .codex/skills -> skills/"
  echo "${repo_diff}" | sed 's/^/  /'
fi

claude_diff="$(rsync -a --delete --dry-run --itemize-changes --exclude '.DS_Store' "${codex_skills}/" "${claude_skills}/" | sed '/^$/d')"
if [ -n "${claude_diff}" ]; then
  diff_found="true"
  echo "Diff: .codex/skills -> .claude/skills/"
  echo "${claude_diff}" | sed 's/^/  /'
fi

if ! cmp -s "${root_dir}/AGENTS.md" "${root_dir}/CLAUDE.md"; then
  diff_found="true"
  echo "Diff: AGENTS.md differs from CLAUDE.md"
fi

if [ -f "${root_dir}/.codex/AGENTS.md" ] && ! cmp -s "${root_dir}/AGENTS.md" "${root_dir}/.codex/AGENTS.md"; then
  diff_found="true"
  echo "Diff: AGENTS.md differs from .codex/AGENTS.md"
fi

if [ -f "${root_dir}/.claude/CLAUDE.md" ] && ! cmp -s "${root_dir}/CLAUDE.md" "${root_dir}/.claude/CLAUDE.md"; then
  diff_found="true"
  echo "Diff: CLAUDE.md differs from .claude/CLAUDE.md"
fi

if [ "${diff_found}" = "true" ] && [ "${force_sync}" != "true" ]; then
  echo "Changes detected. Re-run with --force to apply sync."
  exit 1
fi

rsync -a --delete --exclude '.DS_Store' "${codex_skills}/" "${repo_skills}/"
rsync -a --delete --exclude '.DS_Store' "${codex_skills}/" "${claude_skills}/"

cp "${root_dir}/AGENTS.md" "${root_dir}/CLAUDE.md"
rsync -a --delete "${root_dir}/AGENTS.md" "${root_dir}/.codex/AGENTS.md"
rsync -a --delete "${root_dir}/CLAUDE.md" "${root_dir}/.claude/CLAUDE.md"

echo "Synced skills from .codex/skills to skills/ and .claude/skills; synced AGENTS.md → CLAUDE.md; refreshed .codex/AGENTS.md and .claude/CLAUDE.md"
