# 15. Map-Derived Parity Audit

> Clean-room parity audit comparing the Rust port against map-derived behavior
> surfaces already documented in this repository.
> This document does not reproduce proprietary source code.

---

## Scope

This audit uses three evidence sources already present in the repo:

- [`README.md`](../README.md) for the high-level leaked-source commentary
- [`14_local_binary_diff.md`](14_local_binary_diff.md) for binary-observable capability markers
- the Rust implementation under [`src-rust/`](../src-rust)

Important boundary:

- no Claude Code `.map` artifact is checked into this repository
- no recoverable Claude-specific `.map` file was found on this machine during this audit
- this is therefore a validation against **map-derived clean-room specs and binary markers**, not a byte-for-byte source comparison

---

## Validation Result

The Rust port is **meaningfully aligned** with several high-signal systems surfaced by the `.map`-derived analysis, but it is **not yet a fully complete parity port**.

Best summary:

- core CLI, query-loop, bridge, worktree, hook-streaming, brief messaging, Buddy, and AutoDream concepts are present
- multi-agent orchestration exists, but the public teammate/channel flag surface implied by the leaked build is not fully reproduced
- several internal or feature-gated systems surfaced by the map/binary artifacts remain absent

---

## Parity Matrix

| Surfaced capability | Map-derived signal | Rust status | Evidence |
|---|---|---|---|
| Hook-event streaming | `--include-hook-events` appears in 2.1.88+ | `implemented` | `crates/cli/src/main.rs`, `crates/query/src/lib.rs` |
| UserPromptSubmit enforcement | hook system and blocking semantics documented in specs | `implemented` | `crates/cli/src/main.rs` |
| Bridge / remote control | bridge system strongly surfaced in specs and binaries | `implemented` | `crates/bridge/src/lib.rs`, `crates/commands/src/lib.rs` |
| MCP proxy awareness | `claudeai-mcp`, `mcp-proxy.anthropic.com` markers | `implemented` | `crates/core/src/oauth_config.rs` |
| Worktree support | `--worktree` marker and worktree docs/specs | `partial` | `crates/tools/src/worktree.rs` |
| Brief tool / proactive messaging | KAIROS brief surfaced in specs | `partial` | `crates/tools/src/brief.rs` |
| AutoDream | `autoDream` marker and service docs | `implemented` | `crates/query/src/auto_dream.rs` |
| Buddy | `Buddy` marker and special-systems docs | `implemented` | `crates/buddy/src/lib.rs` |
| Agent/subagent orchestration | teammate/agent markers in specs | `partial` | `crates/query/src/agent_tool.rs`, `crates/query/src/coordinator.rs` |
| Inter-agent messaging | teammate mailbox behavior in specs | `partial` | `crates/tools/src/send_message.rs` |
| Task registry | task/work coordination in specs | `implemented` | `crates/tools/src/tasks.rs`, `crates/core/src/lib.rs` |
| Advisor mode | `--advisor` marker | `missing` | no Rust implementation found |
| Channels flag/surface | `--channels` marker | `missing` | no Rust implementation found |
| Direct teammate CLI flags | `--agent-id`, `--agent-name`, `--team-name`, `--agent-color`, `--parent-session-id`, `--teammate-mode`, `--plan-mode-required` | `missing` | no Rust CLI flag implementation found |
| Direct tmux surface | `--tmux` marker | `missing` | no Rust implementation found |
| ULTRAPLAN | `tengu_ultraplan` marker and command docs | `missing` | no Rust implementation found |
| Undercover mode | README/spec commentary | `missing` | no Rust implementation found |

---

## What Is Solid Today

### 1. Hook-stream parity moved from "surface only" to actual behavior

The local-binary diff surfaced `--include-hook-events` as a public CLI delta.
The Rust port now does the important parts:

- accepts the flag in headless `stream-json` mode
- emits hook lifecycle events
- enforces `UserPromptSubmit` blocking/modification outcomes instead of treating them as telemetry only

That closes the cleanest binary-observable gap.

### 2. Worktree functionality exists, but not as a first-class CLI mode

The leaked/build-surface evidence includes direct worktree-related flags.
The Rust port already supports worktrees as tools:

- `EnterWorktree`
- `ExitWorktree`

This is strong behavioral coverage, but still not full public-surface parity with the embedded `--worktree` flag family.

### 3. Bridge support is substantively present

The bridge subsystem is one of the stronger parity areas:

- runtime config
- token-based activation
- polling loop
- outbound query-event forwarding
- inbound TUI events
- `/remote-control` command surface

This looks like a real port of the bridge family, not a placeholder.

### 4. AutoDream and Buddy are real implementations, not just docs residue

Two features that could easily have been spec-only are actually present:

- AutoDream has gate logic, lock/state files, and prompt construction
- Buddy has its own crate with seeded generation and persistent soul/config handling

That materially increases confidence that the Rust port is trying to cover more than the obvious CLI shell.

---

## Where Parity Is Still Partial

### 1. Multi-agent support is present, but simplified

The Rust port has:

- `AgentTool`
- coordinator prompting
- `SendMessage`
- task registry primitives

But the implementation is still simpler than the teammate/swarm system implied by the map-derived specs:

- `SendMessage` uses an in-process inbox, not the fuller mailbox/socket/tmux ecosystem
- the public teammate CLI flag surface is absent
- there is no evidence of full pane/backend orchestration parity

### 2. Brief exists without the full KAIROS envelope

`Brief` is implemented as a tool, which captures the core message-shaping concept.
What is not yet present is the fuller always-on assistant envelope described in the map-derived docs:

- KAIROS mode
- proactive scheduling/runtime
- KAIROS-only command/feature gating

So this is best considered **concept parity**, not **system parity**.

---

## Clearly Missing Areas

These surfaced areas do not currently appear in the Rust tree as real features:

- advisor configuration and advisor model flow
- channel-specific CLI/runtime surface
- direct teammate identity/session flags
- direct tmux-mode CLI surface
- ULTRAPLAN
- Undercover mode

This means the repo should not currently claim "full parity" with the leaked/build-surfaced Claude Code behavior.

---

## Confidence Notes

Confidence is highest for:

- bridge
- worktree tools
- hook streaming
- AutoDream
- Buddy

Confidence is medium for:

- multi-agent parity overall

Why medium:

- the Rust tree clearly includes agent/coordinator concepts
- but the map-derived specs indicate a richer teammate/channel/tmux world than what is implemented right now

Confidence is low for any claim of full public-surface parity because the embedded flag families observed in the binary are not all exposed in the Rust CLI.

---

## Recommended Next Steps

1. Add a `parity` section to the main README that explicitly says the Rust port is partial, with high-confidence implemented areas and known missing systems.
2. Prioritize the public-surface gaps that already map onto existing concepts:
   - `--worktree`
   - teammate/session identity flags
   - channel gating
3. Decide whether ULTRAPLAN, Undercover, and Advisor are in scope for the Rust rewrite or should stay documented-but-unimplemented.
4. If a real Claude `.map` artifact becomes available locally, run a stricter clean-room audit against:
   - command inventory
   - tool inventory
   - flag inventory
   - feature-gate names

---

## Bottom Line

Using the `.map`-derived materials already checked into this repo, the Rust port validates as:

- **substantial** for core runtime behavior
- **credible** for several advanced subsystems
- **not yet complete** for the broader surfaced CLI/teammate/internal-feature envelope

It is fair to describe the current state as a **serious clean-room reimplementation with meaningful parity**, but not yet a fully validated total port.
