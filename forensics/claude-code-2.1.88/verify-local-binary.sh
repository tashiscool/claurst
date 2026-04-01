#!/usr/bin/env bash

set -euo pipefail

TARGET="${1:-$HOME/.local/share/claude/versions/2.1.88}"
EXPECTED_SHA256="fe0d191adb7b0d26badd1e303e95a63d62d526ca1fb5882f53644754e1e9fe95"

if [[ ! -f "${TARGET}" ]]; then
  echo "Missing binary: ${TARGET}" >&2
  exit 1
fi

echo "Artifact: ${TARGET}"
echo
echo "File type:"
file "${TARGET}"
echo
echo "Reported version:"
"${TARGET}" --version
echo
echo "SHA-256:"
actual_sha="$(shasum -a 256 "${TARGET}" | awk '{print $1}')"
echo "${actual_sha}"
echo

if [[ "${actual_sha}" == "${EXPECTED_SHA256}" ]]; then
  echo "Hash check: OK"
else
  echo "Hash check: MISMATCH" >&2
  echo "Expected: ${EXPECTED_SHA256}" >&2
  exit 2
fi

echo
echo "Code signing:"
codesign -dv --verbose=4 "${TARGET}" 2>&1 | sed -n '1,20p'
