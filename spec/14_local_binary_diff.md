# 14. Local Binary Diff (2.1.87 / 2.1.88 / 2.1.89)

> Clean-room notes generated from locally installed Claude Code binaries on this machine.
> This document summarizes observable behavior, metadata, and implementation clues without reproducing proprietary source.

---

## Scope

This spec covers three locally preserved macOS arm64 binaries:

- `~/.local/share/claude/versions/2.1.87`
- `~/.local/share/claude/versions/2.1.88`
- `~/.local/share/claude/versions/2.1.89`

The binary-analysis workflow lives under [`forensics/claude-code-2.1.88`](/Users/tkhan/IdeaProjects/claude-code/forensics/claude-code-2.1.88), with generated reports in [`reports/version-diff.md`](/Users/tkhan/IdeaProjects/claude-code/forensics/claude-code-2.1.88/reports/version-diff.md).

---

## Evidence Boundary

What this document is based on:

- `--version`
- `--help`
- file metadata, SHA-256, and code-signing metadata
- Mach-O load-command and segment inspection (`otool -l`)
- curated token presence checks against the binary payload

What this document does **not** claim:

- that the local executable itself is source code
- that all embedded strings are user-reachable
- that source-map-related strings inside the Bun payload are equivalent to a redistributable external `.map` file

---

## High-Signal Findings

### 1. `2.1.88` is a real locally preserved release artifact

The recovered `2.1.88` binary:

- reports `2.1.88 (Claude Code)`
- is signed by `Developer ID Application: Anthropic PBC (Q6L2SF6YDW)`
- has SHA-256 `fe0d191adb7b0d26badd1e303e95a63d62d526ca1fb5882f53644754e1e9fe95`

This makes the local copy a better evidentiary artifact than an unverified third-party mirror.

### 2. `--include-hook-events` appears on the public CLI surface in `2.1.88`

Comparing public help output:

- `2.1.87` does **not** expose `--include-hook-events`
- `2.1.88` **does** expose it
- `2.1.89` still exposes it

This is the cleanest CLI-surface delta observed across the three local builds.

### 3. `2.1.88` is smaller than both neighbors, mostly in the Bun payload

Observed file sizes:

- `2.1.87`: `196,638,704`
- `2.1.88`: `196,192,880`
- `2.1.89`: `196,886,384`

The `__TEXT` segment is stable across all three builds.
The main movement is in the `__BUN` segment:

- `2.1.87`: `124,682,240`
- `2.1.88`: `124,239,872`
- `2.1.89`: `124,928,000`

Inference:

- the most significant release-to-release payload churn is happening in bundled Bun-managed application data, not the thin Mach-O wrapper structure

### 4. Source-map-related Bun strings are present in all three binaries

Across `2.1.87`, `2.1.88`, and `2.1.89`, the local binaries all contain these plain-text markers:

- `sourceMappingURL`
- `sourcesContent`
- `sourcemap.json`
- `BUN_FEATURE_FLAG_DISABLE_SOURCE_MAPS`

Inference:

- source-map support machinery and related string literals remain embedded in the Bun payload
- this observation alone does **not** prove that an external source map is still recoverable from the local executable

### 5. Embedded capability strings are broader than the public help surface

All three binaries contain strings for features or flags including:

- `--advisor`
- `--enable-auto-mode`
- `--channels`
- `--dangerously-load-development-channels`
- `--agent-id`
- `--agent-name`
- `--team-name`
- `--agent-color`
- `--plan-mode-required`
- `--parent-session-id`
- `--teammate-mode`
- `--worktree`
- `--tmux`

They also contain implementation markers such as:

- `tengu_ultraplan`
- `claudeai-mcp`
- `https://mcp-proxy.anthropic.com`
- `autoDream`
- `Buddy`
- `claude-sonnet-4-6`

Inference:

- the local binaries preserve evidence of teammate/channel/worktree/advisor-style flows and internal implementation families beyond the subset of options visible in `--help`

---

## Rust Port Parity Notes

### Landed in this branch

The Rust CLI now exposes `--include-hook-events` in headless `stream-json` mode and emits hook-event JSON for:

- `UserPromptSubmit`
- `PreToolUse`
- `PostToolUse`
- `Stop`

Relevant implementation files:

- [`src-rust/crates/cli/src/main.rs`](/Users/tkhan/IdeaProjects/claude-code/src-rust/crates/cli/src/main.rs)
- [`src-rust/crates/query/src/lib.rs`](/Users/tkhan/IdeaProjects/claude-code/src-rust/crates/query/src/lib.rs)

### Already present in the Rust port

- `stream-json` output mode exists
- worktree support exists as tools (`EnterWorktree`, `ExitWorktree`)
- plugin hook infrastructure already exists and supports multiple hook events

### Still missing or only partially represented

- public CLI parity for teammate/channel/advisor-style flags observed in the bundled binaries
- parity for direct CLI worktree/tmux flags observed as embedded strings
- richer channel and multi-agent coordination surfaces implied by the binary strings

---

## Recommended Follow-Ups

1. Promote this local diff workflow into a repeatable regression check for future binary snapshots.
2. Add a small parity matrix mapping observable binary features to Rust implementation status.
3. Prioritize the subset of embedded flags that correspond to already-existing Rust concepts, especially worktree and hook-streaming behavior.

---

## Reproduction

Generate the report again with:

```bash
cd forensics/claude-code-2.1.88
./analyze_versions.py
```
