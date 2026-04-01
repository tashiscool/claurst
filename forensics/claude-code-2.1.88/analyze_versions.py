#!/usr/bin/env python3

from __future__ import annotations

import hashlib
import json
import mmap
import re
import stat
import subprocess
import sys
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Dict, List


DEFAULT_VERSIONS = ["2.1.87", "2.1.88", "2.1.89"]
DEFAULT_BASE = Path.home() / ".local" / "share" / "claude" / "versions"
REPORTS_DIR = Path(__file__).resolve().parent / "reports"

EMBEDDED_FLAGS = [
    "--include-hook-events",
    "--advisor",
    "--enable-auto-mode",
    "--channels",
    "--dangerously-load-development-channels",
    "--agent-id",
    "--agent-name",
    "--team-name",
    "--agent-color",
    "--plan-mode-required",
    "--parent-session-id",
    "--teammate-mode",
    "--worktree",
    "--tmux",
]

SOURCE_MAP_MARKERS = [
    "sourceMappingURL",
    "sourcesContent",
    "sourcemap.json",
    "BUN_FEATURE_FLAG_DISABLE_SOURCE_MAPS",
]

IMPLEMENTATION_MARKERS = [
    "tengu_ultraplan",
    "claudeai-mcp",
    "https://mcp-proxy.anthropic.com",
    "autoDream",
    "Buddy",
    "claude-sonnet-4-6",
]

SEGMENTS = ["__TEXT", "__BUN", "__LINKEDIT", "__DATA_CONST", "__DATA"]


@dataclass
class ArtifactInfo:
    version: str
    path: str
    size_bytes: int
    mtime: str
    sha256: str
    file_type: str
    reported_version: str
    codesign: Dict[str, str]
    segments: Dict[str, Dict[str, int]]
    public_help_flags: List[str]
    embedded_flags: Dict[str, bool]
    source_map_markers: Dict[str, bool]
    implementation_markers: Dict[str, bool]


def run(cmd: List[str]) -> str:
    proc = subprocess.run(cmd, capture_output=True, text=True, check=True)
    return proc.stdout if proc.stdout else proc.stderr


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def contains_token(path: Path, token: str) -> bool:
    needle = token.encode()
    with path.open("rb") as handle:
        with mmap.mmap(handle.fileno(), 0, access=mmap.ACCESS_READ) as mm:
            return mm.find(needle) != -1


def parse_codesign(path: Path) -> Dict[str, str]:
    text = run(["codesign", "-dv", "--verbose=4", str(path)])
    wanted = {"Identifier", "Authority", "Timestamp", "TeamIdentifier"}
    data: Dict[str, str] = {}
    authorities: List[str] = []
    for line in text.splitlines():
        if "=" not in line:
            continue
        key, value = line.split("=", 1)
        if key == "Authority":
            authorities.append(value.strip())
        elif key in wanted:
            data[key] = value.strip()
    if authorities:
        data["Authority"] = "; ".join(authorities)
    return data


def parse_segments(path: Path) -> Dict[str, Dict[str, int]]:
    lines = run(["otool", "-l", str(path)]).splitlines()
    segments: Dict[str, Dict[str, int]] = {}
    current = None
    for raw in lines:
        line = raw.strip()
        if line.startswith("segname "):
            current = line.split()[1]
            if current in SEGMENTS:
                segments.setdefault(current, {})
        elif current in SEGMENTS and line.startswith("vmsize "):
            value = line.split()[1]
            segments[current]["vmsize"] = int(value, 16) if value.startswith("0x") else int(value)
        elif current in SEGMENTS and line.startswith("filesize "):
            value = line.split()[1]
            segments[current]["filesize"] = int(value, 16) if value.startswith("0x") else int(value)
    return segments


def parse_help_flags(path: Path) -> List[str]:
    text = run([str(path), "--help"])
    flags: List[str] = []
    for line in text.splitlines():
        if not line.startswith("  "):
            continue
        match = re.match(r"^\s{2}(.+?)\s{2,}\S", line)
        if not match:
            continue
        flag_candidates = re.findall(r"--[A-Za-z0-9][A-Za-z0-9-]*", match.group(1))
        flags.extend(flag_candidates)
    return sorted(set(flags))


def file_type(path: Path) -> str:
    return run(["file", str(path)]).strip()


def analyze_version(version: str, path: Path) -> ArtifactInfo:
    st = path.stat()
    return ArtifactInfo(
        version=version,
        path=str(path),
        size_bytes=st.st_size,
        mtime=datetime.fromtimestamp(st.st_mtime).isoformat(),
        sha256=sha256(path),
        file_type=file_type(path),
        reported_version=run([str(path), "--version"]).strip(),
        codesign=parse_codesign(path),
        segments=parse_segments(path),
        public_help_flags=parse_help_flags(path),
        embedded_flags={token: contains_token(path, token) for token in EMBEDDED_FLAGS},
        source_map_markers={token: contains_token(path, token) for token in SOURCE_MAP_MARKERS},
        implementation_markers={
            token: contains_token(path, token) for token in IMPLEMENTATION_MARKERS
        },
    )


def markdown_report(artifacts: List[ArtifactInfo]) -> str:
    by_version = {artifact.version: artifact for artifact in artifacts}
    versions = [artifact.version for artifact in artifacts]

    def segment_table() -> str:
        lines = ["| Version | __TEXT | __BUN | __LINKEDIT |", "| --- | ---: | ---: | ---: |"]
        for artifact in artifacts:
            text = artifact.segments.get("__TEXT", {}).get("filesize", 0)
            bun = artifact.segments.get("__BUN", {}).get("filesize", 0)
            linkedit = artifact.segments.get("__LINKEDIT", {}).get("filesize", 0)
            lines.append(
                f"| {artifact.version} | {text:,} | {bun:,} | {linkedit:,} |"
            )
        return "\n".join(lines)

    flags_87 = set(by_version["2.1.87"].public_help_flags)
    flags_88 = set(by_version["2.1.88"].public_help_flags)
    flags_89 = set(by_version["2.1.89"].public_help_flags)
    added_87_88 = sorted(flags_88 - flags_87)
    removed_88_89 = sorted(flags_88 - flags_89)
    added_88_89 = sorted(flags_89 - flags_88)

    lines = [
        "# Local Claude Code Binary Diff",
        "",
        "Generated from locally installed binaries on this machine.",
        "",
        "## Artifacts",
        "",
        "| Version | Size (bytes) | SHA-256 | Reported version |",
        "| --- | ---: | --- | --- |",
    ]
    for artifact in artifacts:
        lines.append(
            f"| {artifact.version} | {artifact.size_bytes:,} | `{artifact.sha256}` | `{artifact.reported_version}` |"
        )

    lines.extend(
        [
            "",
            "## Public CLI Diff",
            "",
            f"- `2.1.87 -> 2.1.88` added help flags: {', '.join(f'`{f}`' for f in added_87_88) if added_87_88 else 'none'}",
            f"- `2.1.88 -> 2.1.89` added help flags: {', '.join(f'`{f}`' for f in added_88_89) if added_88_89 else 'none'}",
            f"- `2.1.88 -> 2.1.89` removed help flags: {', '.join(f'`{f}`' for f in removed_88_89) if removed_88_89 else 'none'}",
            "",
            "## Embedded Flag Presence",
            "",
            "| Flag | 2.1.87 | 2.1.88 | 2.1.89 |",
            "| --- | --- | --- | --- |",
        ]
    )
    for flag in EMBEDDED_FLAGS:
        lines.append(
            f"| `{flag}` | {'yes' if by_version['2.1.87'].embedded_flags[flag] else 'no'} | {'yes' if by_version['2.1.88'].embedded_flags[flag] else 'no'} | {'yes' if by_version['2.1.89'].embedded_flags[flag] else 'no'} |"
        )

    lines.extend(
        [
            "",
            "## Source-Map Related String Markers",
            "",
            "| Marker | 2.1.87 | 2.1.88 | 2.1.89 |",
            "| --- | --- | --- | --- |",
        ]
    )
    for marker in SOURCE_MAP_MARKERS:
        lines.append(
            f"| `{marker}` | {'yes' if by_version['2.1.87'].source_map_markers[marker] else 'no'} | {'yes' if by_version['2.1.88'].source_map_markers[marker] else 'no'} | {'yes' if by_version['2.1.89'].source_map_markers[marker] else 'no'} |"
        )

    lines.extend(
        [
            "",
            "## Implementation Marker Presence",
            "",
            "| Marker | 2.1.87 | 2.1.88 | 2.1.89 |",
            "| --- | --- | --- | --- |",
        ]
    )
    for marker in IMPLEMENTATION_MARKERS:
        lines.append(
            f"| `{marker}` | {'yes' if by_version['2.1.87'].implementation_markers[marker] else 'no'} | {'yes' if by_version['2.1.88'].implementation_markers[marker] else 'no'} | {'yes' if by_version['2.1.89'].implementation_markers[marker] else 'no'} |"
        )

    lines.extend(
        [
            "",
            "## Segment Sizes",
            "",
            segment_table(),
            "",
            "## Notes",
            "",
            "- `2.1.88` is smaller than both `2.1.87` and `2.1.89`, and the delta is concentrated in the `__BUN` segment.",
            "- The public `--help` surface shows `--include-hook-events` appearing in `2.1.88` and remaining in `2.1.89`.",
            "- All three local binaries still contain plain string markers related to source maps and Bun source-map support, but that is not equivalent to shipping a recoverable `.map` artifact alongside the local executable.",
            "- The binaries also carry embedded strings for teammate, channel, advisor, worktree, and tmux-style features that are not all surfaced in the public help output.",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> int:
    versions = sys.argv[1:] if len(sys.argv) > 1 else DEFAULT_VERSIONS
    artifacts: List[ArtifactInfo] = []
    for version in versions:
        path = DEFAULT_BASE / version
        if not path.exists():
            raise SystemExit(f"Missing local artifact: {path}")
        artifacts.append(analyze_version(version, path))

    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    json_report = {
        "generated_at": datetime.now(UTC).isoformat().replace("+00:00", "Z"),
        "artifacts": [artifact.__dict__ for artifact in artifacts],
    }
    (REPORTS_DIR / "version-diff.json").write_text(
        json.dumps(json_report, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (REPORTS_DIR / "version-diff.md").write_text(
        markdown_report(artifacts),
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
