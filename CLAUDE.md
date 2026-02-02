# OpenClaw Development Guidelines

- Repo: https://github.com/openclaw/openclaw

## Project Structure

- Source: `src/` (CLI in `src/cli`, commands in `src/commands`, infra in `src/infra`, media in `src/media`)
- Tests: colocated `*.test.ts`
- Docs: `docs/` (Mintlify, hosted at docs.openclaw.ai). Built output in `dist/`.
- Plugins/extensions: `extensions/*` (workspace packages). Plugin deps stay in extension `package.json`.
- Channels: `src/telegram`, `src/discord`, `src/slack`, `src/signal`, `src/imessage`, `src/web`, `src/channels`, `src/routing` + `extensions/*`

## Build & Dev

- Node **22+**; prefer Bun for TS execution (`bun <file.ts>`)
- Install: `pnpm install`
- Dev: `pnpm openclaw ...` or `pnpm dev`
- Build: `pnpm build`
- Lint: `pnpm lint` (oxlint), Format: `pnpm format` (oxfmt)
- Test: `pnpm test` (vitest), Coverage: `pnpm test:coverage`

## Coding Style

- TypeScript (ESM). Strict typing; avoid `any`.
- Run `pnpm lint` before commits.
- Keep files under ~500-700 LOC; split when it improves clarity.
- Brief comments for tricky logic only.
- Naming: **OpenClaw** for product/headings; `openclaw` for CLI/package/paths/config.
- CLI progress: use `src/cli/progress.ts`; don't hand-roll spinners.
- Colors: use shared palette in `src/terminal/palette.ts`.
- Tool schemas: no `Type.Union`; use `stringEnum`/`optionalStringEnum`. No raw `format` property names.

## Commits & PRs

- Commit with `scripts/committer "<msg>" <file...>` to keep staging scoped.
- Concise action-oriented messages (e.g., `CLI: add verbose flag to send`).
- PR review: use `gh pr view`/`gh pr diff`; do not switch branches.
- Changelog: keep latest released version at top; reference issue/PR numbers.
- Never commit real phone numbers, videos, or live config values.

## Testing

- Vitest; V8 coverage thresholds (70%).
- Test naming: `*.test.ts`; e2e: `*.e2e.test.ts`
- Run tests before pushing when touching logic.

## Docs

- Internal links: root-relative, no `.md` suffix (e.g., `[Config](/configuration)`)
- Avoid em dashes/apostrophes in headings (breaks Mintlify anchors)
- Keep docs generic; use placeholders instead of real device names/paths

## Key Rules

- Never edit `node_modules`.
- Never update the Carbon dependency.
- Patched deps (`pnpm.patchedDependencies`) must use exact versions (no `^`/`~`).
- Dependency patching requires explicit approval.
- Verify answers in code; do not guess.
- For technical analysis tables, follow `technical-analysis/TABLE_FORMAT.md`.
- Do not change version numbers without explicit consent.