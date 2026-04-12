# Claude Code 2.1.88 Local Artifact Notes

This directory documents a locally recovered `Claude Code 2.1.88` executable that already exists on this Mac at:

```text
/Users/tkhan/.local/share/claude/versions/2.1.88
```

## What This Is

- a locally installed `Claude Code 2.1.88` Mach-O executable
- a reproducible verification workflow for that local artifact
- a place to keep private local copies out of git if you choose to archive them

## What This Is Not

- not a claim that the executable itself is source code
- not a redistributed copy of proprietary source
- not proof that this repo contains Anthropic's original TypeScript sources

The recovered file is an Apple-signed arm64 binary.
On this machine it reports:

```text
2.1.88 (Claude Code)
```

## Known Fingerprints

- path: `/Users/tkhan/.local/share/claude/versions/2.1.88`
- file type: `Mach-O 64-bit executable arm64`
- SHA-256: `fe0d191adb7b0d26badd1e303e95a63d62d526ca1fb5882f53644754e1e9fe95`
- bundle identifier: `com.anthropic.claude-code`
- signing authority: `Developer ID Application: Anthropic PBC (Q6L2SF6YDW)`
- signing timestamp: `Mar 30, 2026 at 6:20:05 PM`

## Why This Matters

The local binary is useful as a preserved artifact for:

- version comparison against `2.1.87` and `2.1.89`
- behavior testing
- metadata and signature verification
- documenting what was actually present on disk during the `2.1.88` window

It is not sufficient, by itself, to claim that you have "actual source code."
For that, you would need a source-bearing artifact such as:

- an official public source repository
- a source archive
- a package that still includes source files or source maps

## Verify The Local Artifact

Run:

```bash
./verify-local-binary.sh
```

Or against a different path:

```bash
./verify-local-binary.sh /path/to/claude-code-binary
```

## Compare Local Versions

Generate a local diff report for `2.1.87`, `2.1.88`, and `2.1.89`:

```bash
./analyze_versions.py
```

This writes:

- `reports/version-diff.json`
- `reports/version-diff.md`

## Optional Private Archive

If you want a private local copy inside this repo without committing the binary:

```bash
mkdir -p local
cp /Users/tkhan/.local/share/claude/versions/2.1.88 local/claude-code-2.1.88
zip -j local/claude-code-2.1.88.zip local/claude-code-2.1.88
```

The `local/` directory is gitignored by this directory's `.gitignore`.
