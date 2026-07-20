"""Bump an app's manifest.json version from Conventional Commit subjects.

Usage: python auto_version.py <app_dir> < commit_subjects.txt

Reads commit subject lines from stdin (one per line), picks the highest
semver bump implied by them, and rewrites <app_dir>/manifest.json in place.
Prints the resulting version. If no subject implies a bump, leaves the file
untouched and prints the current version.
"""

import json
import re
import sys

COMMIT_RE = re.compile(r"^(\w+)(\([\w.-]+\))?(!)?:")
VERSION_RE = re.compile(r'("version"\s*:\s*")\d+\.\d+\.\d+(")')

# ponytail: breaking changes only bump major once major > 0 (semver "initial
# development" rule) — reaching 1.0.0 is a deliberate manual edit, not inferred.
RANK = {"none": 0, "patch": 1, "minor": 2, "major": 3}


def bump_type(subject: str) -> str:
    match = COMMIT_RE.match(subject.strip())
    if not match:
        return "none"
    commit_type, _, breaking = match.groups()
    if commit_type == "fix":
        return "patch"
    if commit_type == "feat":
        return "major" if breaking else "minor"
    return "none"


def highest_bump(subjects: list[str]) -> str:
    return max((bump_type(s) for s in subjects), key=RANK.__getitem__, default="none")


def apply_bump(version: str, bump: str) -> str:
    major, minor, patch = (int(part) for part in version.split("."))
    if bump == "major" and major > 0:
        return f"{major + 1}.0.0"
    if bump in ("major", "minor"):
        return f"{major}.{minor + 1}.0"
    if bump == "patch":
        return f"{major}.{minor}.{patch + 1}"
    return version


def bump_manifest(manifest_path: str, subjects: list[str]) -> str:
    with open(manifest_path, encoding="utf-8") as f:
        text = f.read()

    current_version = json.loads(text)["version"]
    new_version = apply_bump(current_version, highest_bump(subjects))

    if new_version != current_version:
        text = VERSION_RE.sub(rf"\g<1>{new_version}\g<2>", text, count=1)
        with open(manifest_path, "w", encoding="utf-8", newline="\n") as f:
            f.write(text)

    return new_version


def main() -> None:
    app_dir = sys.argv[1]
    subjects = [line for line in sys.stdin.read().splitlines() if line.strip()]
    print(bump_manifest(f"{app_dir}/manifest.json", subjects))


if __name__ == "__main__":
    main()
