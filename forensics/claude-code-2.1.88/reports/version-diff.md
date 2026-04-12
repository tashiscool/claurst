# Local Claude Code Binary Diff

Generated from locally installed binaries on this machine.

## Artifacts

| Version | Size (bytes) | SHA-256 | Reported version |
| --- | ---: | --- | --- |
| 2.1.87 | 196,638,704 | `80b51562db1a51bfb654aec1fea6a04106daa0bc1525d88c9c74741ff5d9469a` | `2.1.87 (Claude Code)` |
| 2.1.88 | 196,192,880 | `fe0d191adb7b0d26badd1e303e95a63d62d526ca1fb5882f53644754e1e9fe95` | `2.1.88 (Claude Code)` |
| 2.1.89 | 196,886,384 | `f903a5e53f845b1ac5566296b713193827665f28da16300fdca7539cb0669a7f` | `2.1.89 (Claude Code)` |

## Public CLI Diff

- `2.1.87 -> 2.1.88` added help flags: `--include-hook-events`
- `2.1.88 -> 2.1.89` added help flags: none
- `2.1.88 -> 2.1.89` removed help flags: none

## Embedded Flag Presence

| Flag | 2.1.87 | 2.1.88 | 2.1.89 |
| --- | --- | --- | --- |
| `--include-hook-events` | no | yes | yes |
| `--advisor` | yes | yes | yes |
| `--enable-auto-mode` | yes | yes | yes |
| `--channels` | yes | yes | yes |
| `--dangerously-load-development-channels` | yes | yes | yes |
| `--agent-id` | yes | yes | yes |
| `--agent-name` | yes | yes | yes |
| `--team-name` | yes | yes | yes |
| `--agent-color` | yes | yes | yes |
| `--plan-mode-required` | yes | yes | yes |
| `--parent-session-id` | yes | yes | yes |
| `--teammate-mode` | yes | yes | yes |
| `--worktree` | yes | yes | yes |
| `--tmux` | yes | yes | yes |

## Source-Map Related String Markers

| Marker | 2.1.87 | 2.1.88 | 2.1.89 |
| --- | --- | --- | --- |
| `sourceMappingURL` | yes | yes | yes |
| `sourcesContent` | yes | yes | yes |
| `sourcemap.json` | yes | yes | yes |
| `BUN_FEATURE_FLAG_DISABLE_SOURCE_MAPS` | yes | yes | yes |

## Implementation Marker Presence

| Marker | 2.1.87 | 2.1.88 | 2.1.89 |
| --- | --- | --- | --- |
| `tengu_ultraplan` | yes | yes | yes |
| `claudeai-mcp` | yes | yes | yes |
| `https://mcp-proxy.anthropic.com` | yes | yes | yes |
| `autoDream` | yes | yes | yes |
| `Buddy` | yes | yes | yes |
| `claude-sonnet-4-6` | yes | yes | yes |

## Segment Sizes

| Version | __TEXT | __BUN | __LINKEDIT |
| --- | ---: | ---: | ---: |
| 2.1.87 | 68,501,504 | 124,682,240 | 1,767,408 |
| 2.1.88 | 68,501,504 | 124,239,872 | 1,763,952 |
| 2.1.89 | 68,501,504 | 124,928,000 | 1,769,328 |

## Notes

- `2.1.88` is smaller than both `2.1.87` and `2.1.89`, and the delta is concentrated in the `__BUN` segment.
- The public `--help` surface shows `--include-hook-events` appearing in `2.1.88` and remaining in `2.1.89`.
- All three local binaries still contain plain string markers related to source maps and Bun source-map support, but that is not equivalent to shipping a recoverable `.map` artifact alongside the local executable.
- The binaries also carry embedded strings for teammate, channel, advisor, worktree, and tmux-style features that are not all surfaced in the public help output.
