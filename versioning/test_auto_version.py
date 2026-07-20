import tempfile
from pathlib import Path

from auto_version import apply_bump, bump_manifest, highest_bump

EXAMPLE_MANIFEST = """{
  "name": "demo-app",
  "description": "An example app",
  "version": "0.1.0",
  "docker_repo": "salillas/demo-app",
  "endpoint": { "path": "/", "method": "GET" },
  "tags": ["demo"]
}
"""


def test_highest_bump_picks_the_biggest():
    assert highest_bump(["chore: cleanup", "fix: x", "feat: y"]) == "minor"
    assert highest_bump(["fix: x", "fix: y"]) == "patch"
    assert highest_bump(["chore: cleanup", "docs: x"]) == "none"
    assert highest_bump(["feat!: breaking"]) == "major"


def test_apply_bump_pre_1_0_treats_breaking_as_minor():
    assert apply_bump("0.1.0", "major") == "0.2.0"


def test_apply_bump_post_1_0_bumps_major():
    assert apply_bump("1.2.3", "major") == "2.0.0"


def test_apply_bump_minor_resets_patch():
    assert apply_bump("1.2.3", "minor") == "1.3.0"


def test_apply_bump_patch():
    assert apply_bump("1.2.3", "patch") == "1.2.4"


def test_apply_bump_none_is_noop():
    assert apply_bump("1.2.3", "none") == "1.2.3"


def test_bump_manifest_only_touches_the_version_line():
    with tempfile.TemporaryDirectory() as tmp:
        manifest_path = Path(tmp) / "manifest.json"
        manifest_path.write_text(EXAMPLE_MANIFEST, encoding="utf-8")

        new_version = bump_manifest(
            str(manifest_path), ["chore: tidy imports", "feat: add /random endpoint"]
        )

        assert new_version == "0.2.0"
        updated = manifest_path.read_text(encoding="utf-8")
        assert updated == EXAMPLE_MANIFEST.replace('"0.1.0"', '"0.2.0"')


def test_bump_manifest_is_a_noop_without_a_bump():
    with tempfile.TemporaryDirectory() as tmp:
        manifest_path = Path(tmp) / "manifest.json"
        manifest_path.write_text(EXAMPLE_MANIFEST, encoding="utf-8")

        new_version = bump_manifest(str(manifest_path), ["chore: tidy imports"])

        assert new_version == "0.1.0"
        assert manifest_path.read_text(encoding="utf-8") == EXAMPLE_MANIFEST


if __name__ == "__main__":
    test_highest_bump_picks_the_biggest()
    test_apply_bump_pre_1_0_treats_breaking_as_minor()
    test_apply_bump_post_1_0_bumps_major()
    test_apply_bump_minor_resets_patch()
    test_apply_bump_patch()
    test_apply_bump_none_is_noop()
    test_bump_manifest_only_touches_the_version_line()
    test_bump_manifest_is_a_noop_without_a_bump()
    print("ok")
